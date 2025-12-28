"""
MANTIS - Kernel
"""

import subprocess
import os
import sys
import time
import getpass

from mantis.event_bus import EventBus
from mantis.logger import setup_logger
from mantis.context import Context
from mantis.skill_router import SkillRouter
import mantis.skills
from mantis.skills.registry import SKILL_REGISTRY
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


class Kernel:
    def __init__(self):
        self.running = False
        self.logger = setup_logger()

        self.context = Context()
        
        self.event_bus = EventBus()

        self.skills = [skill_cls() for skill_cls in SKILL_REGISTRY]

        self.router = SkillRouter(self.skills)
        print("[KERNEL] Loaded Skills]:", [s.name for s in self.skills])

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


    def restart(self):
        self.logger.info("Redémarrage de Mantis")

        python = sys.executable
        subprocess.Popen(
            [python, "-m", "mantis"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        self.stop()


    def on_system_start(self, payload=None):
        self.context.set("system.status", "running")
        self.context.set("user", getpass.getuser())
        self.context.set("introduced", False)
        
        self.logger.info(f"Context initialized : {self.context.dump()}")


    def on_intent(self, intent):
        self.logger.info(
            f"Intent received: {intent.name}"
            f"(source={intent.source}, confidence={intent.confidence})"
            )

        introduced = self.context.get("introduced", False)

        result = self.router.route(intent, self.context)

        if result is not None:
            response = self.response_builder.build(intent, result)

            text = self.nlg.generate(
                response=response,
                introduce=not introduced
            )
        
        else:
            text = self.nlg.generate(
                user_text=intent.raw,
                introduce=not introduced
            )
            
        if not introduced:
            self.context.set("introduced", True)

        self.logger.info(f"Final response generated")
        self.logger.info(
            f"INTRODUCE={not introduced} | introduced={introduced}"
        )
        return text
    

    def cli_loop(self):
        self.logger.info("CLI ready. Type 'exit' to quit.")

        while self.running:
            try:
                text = input("> ")

                if text.strip().lower() in ("exit", "quit"):
                    self.stop()
                    return
                
                if text.strip().lower() in ("restart", "reload", "load"):
                    self.restart()
                    return
                
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
                    self.tts.speak(response)

            except (EOFError, KeyboardInterrupt):
                self.stop()
                return