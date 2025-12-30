"""
MANTIS - Kernel
"""

import subprocess
import os
import sys
import time
import getpass
import time

from enum import Enum, auto

from mantis.event_bus import EventBus
from mantis.logger import setup_logger
from mantis.context import Context
from mantis.skill_router import SkillRouter
import mantis.skills
from mantis.skills.registry import SKILL_REGISTRY
from mantis.permissions import UserPermission
from mantis.permission_policy import PermissionPolicy
from mantis.intent import Intent
from mantis.intent_parser import IntentParser
from mantis.response import ResponseBuilder
from mantis.nlg.templates import TemplatesNLG
from mantis.nlg.ollama import OllamaNLG
from mantis.tts.piper import PiperTTS
from mantis.tts.dummy import DummyTTS

LOCK_FILE = "mantis.lock"
def pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return False
    
class KernelState(Enum):
    STARTING = auto()
    RUNNING = auto()
    SHUTTING_DOWN = auto()
    STOPPED = auto()

class Kernel:
    def __init__(self):
        self.state = KernelState.STARTING

        self.running = False
        self.logger = setup_logger()

        self.override_permission = None
        self.override_until = None

        self.user_permissions_by_source = {
            "cli": UserPermission.USER,
            "voice": UserPermission.USER,
            "ha": UserPermission.USER,
        }

        self.permission_policy = PermissionPolicy()

        self.context = Context()
        
        self.event_bus = EventBus()

        self.skills = []
        for skill_cls in SKILL_REGISTRY:
            skill = skill_cls()
            skill.kernel = self
            self.skills.append(skill)

        self.router = SkillRouter(self.skills)
        print("[KERNEL] [Loaded Skills]:", [s.name for s in self.skills])

        self.event_bus.subscribe("system.start", self.on_system_start)
        #self.event_bus.subscribe("intent.received", self.on_intent)

        self.intent_parser = IntentParser()

        self.response_builder = ResponseBuilder()

        ENABLE_LLM = False
        if ENABLE_LLM:
            self.nlg = OllamaNLG(model="mistral")
        else:
            self.nlg = TemplatesNLG()
        
        ENABLE_TTS = True
        if ENABLE_TTS:
            self.tts = PiperTTS(
                piper_path=r"C:\piper\piper.exe",
                model_path=r"C:\piper\voices\fr_FR-upmc-medium.onnx"
            )
        else:
            self.tts = DummyTTS()

        self.state = KernelState.RUNNING


    def start(self):
        try:
            self.lock_fd = os.open(
                LOCK_FILE,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY
            )
            os.write(self.lock_fd, str(os.getpid()).encode())
        except FileExistsError:
            self.logger.error("Another instance of Mantis is already running. Exiting")
            sys.exit(1)

        self.running = True
        self.logger.info("Kernel started")

        # Emit startup event
        self.event_bus.emit("system.start")

        self.cli_loop()

        while self.running:
            time.sleep(1)


    def stop(self, *_):
        self.logger.info("Kernel stopping...")
        self.running = False
        
        try:
            os.close(self.lock_fd)
            os.remove(LOCK_FILE)
        except Exception:
            pass

        sys.exit(0)


    def restart(self, reason: str="unknown"):
        self.logger.info("Redémarrage de Mantis")

        python = sys.executable
        subprocess.Popen(
            [python, "-m", "mantis"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        self.stop()

    def shutdown(self, reason: str="unknown"):
        if self.state == KernelState.SHUTTING_DOWN:
            return
        
        self.logger.info(f"Shutdown requested: {reason}")
        self.state = KernelState.SHUTTING_DOWN

        if hasattr(self.event_bus, "shutdown"):
            self.event_bus.shutdown()

        for skill in self.skills:
            if hasattr(skill, "shutdown"):
                try:
                    skill.shutdown()
                except Exception as e:
                    self.logger.error(f"Skill {skill.__class__.__name__} shutdown failed: {e}")

        if hasattr(self, "lock_fd"):
            try:
                os.close(self.lock_fd)
                os.remove(LOCK_FILE)
            except Exception:
                pass

        self.running = False
        self.state = KernelState.STOPPED
        sys.exit(0)


    def on_system_start(self, payload=None):
        self.context.set("system.status", "running")
        self.context.set("user", getpass.getuser())
        self.context.set("introduced", False)
        
        self.logger.info(f"Context initialized : {self.context.dump()}")


    def on_intent(self, intent):
        # 1. Identify user
        base_user_perm = self._identify_user(intent)
        effective_user_perm = self.get_effective_user_permission(base_user_perm)
        self.logger.debug(f"[USER] source){intent.source} permission={effective_user_perm.name}")

        # 2. Log intent reception
        self.logger.info(
            f"Intent received: {intent.name}" 
            f"(source={intent.source}, confidence={intent.confidence})"
        )

        # 3. Route skill
        skill = self._route_skill(intent)
        if not skill: 
            self.logger.info(
                f"No skill found for intent: {intent.name}"
            ) 
            return None
        
        # 4. Permission check
        decision = self.permission_policy.check(
            user_permission=effective_user_perm,
            skill_permission=skill.permission,
            context=self.context,
        )

        self.logger.info(
            f"[POLICY] user={effective_user_perm.name} "
            f"skill={skill.name} "
            f"decision={'ALLOW' if decision.allowed else 'DENY'} "
            f"reason={decision.reason}"
        )

        if not decision.allowed:
            return "Désolé, vous n'avez pas la permission pour cette action."

        # 5. Execute skill
        try:
            result = self._execute_skill(skill, intent)
            return result
        except Exception as e:
            self.logger.error(
                f"[ERROR] Skill {skill.name} execution failed: {e}"
            )
            return "Une erreur est survenue lors de l'éxecution de l'action."
    
    def _route_skill(self,intent):
        return self.router.route(intent, self.context)
    
    def _execute_skill(self, skill, intent):
        return skill.execute(intent, self.context)

    def _identify_user(self, intent):
        return self.get_user_permission(intent)

    def get_user_permission(self, intent):
        return self.user_permissions_by_source.get(
            intent.source,
            UserPermission.GUEST
        )   

    def enable_override(self, permission, duration_seconds: int):
        self.override_permission = permission
        self.override_until = time.time() + duration_seconds
        self.logger.warning(
            f"[OVERRIDE] Permission elevated to {permission.name} "
            f"for {duration_seconds}s"
        )

    def clear_override(self):
        self.logger.warning("[OVERRIDE] Permission override cleared")
        self.override_permission = None
        self.override_until = None

    def get_effective_user_permission(self, base_permission):
        if self.override_permission and self.override_until:
            if time.time() < self.override_until:
                return self.override_permission
            else:
                self.clear_override()
        return base_permission

    def cli_loop(self):
        self.logger.info("CLI ready. Type 'exit' to quit.")

        while self.running:
            try:
                text = input("> ")
                
                intent = self.intent_parser.parse(text)

                if intent is None:
                    intent = Intent(
                        name="unknown",
                        raw=text,
                        source="cli",
                        confidence=0.0
                    )

                response = self.on_intent(intent)

                if response:
                    print(response)

                    if isinstance(response, str):
                        self.tts.speak(response)

            except (EOFError, KeyboardInterrupt):
                intent = Intent(
                    name="system.shutdown",
                    raw="exit"
                )
                return