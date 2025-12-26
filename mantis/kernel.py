"""
MANTIS Kernel
Core lifecycle manager
"""

import sys
import time
import getpass
from mantis.event_bus import EventBus
from mantis.logger import setup_logger
from mantis.context import Context
from mantis.skill_router import SkillRouter
from mantis.skills.system import SystemSkill
from mantis.intent import Intent
from mantis.intent_parser import IntentParser
from mantis.response import ResponseBuilder
from mantis.nlg.templates import TemplatesNLG
from mantis.nlg.ollama import OllamaNLG
from mantis.tts.piper import PiperTTS


class Kernel:
    def __init__(self):
        self.running = False
        self.logger = setup_logger()

        self.context = Context()
        self.event_bus = EventBus()

        self.skills = [
            SystemSkill(),
        ]
        self.router = SkillRouter(self.skills)

        self.event_bus.subscribe("system.start", self.on_system_start)
        #self.event_bus.subscribe("intent.received", self.on_intent)

        self.intent_parser = IntentParser()

        self.response_builder = ResponseBuilder()

        self.nlg = OllamaNLG(model="mistral")

        self.tts = PiperTTS(
            piper_path=r"C:\piper\piper.exe",
            model_path=r"C:\piper\voices\fr_FR-upmc-medium.onnx"
        )


    def start(self):
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
        sys.exit(0)


    def on_system_start(self, payload=None):
        self.context.set("system.status", "running")
        self.context.set("user", getpass.getuser())
        
        self.logger.info(f"Context initialized : {self.context.dump()}")


    def on_intent(self, intent):
        self.logger.info(
            f"Intent received: {intent.name}"
            f"(source={intent.source}, confidence={intent.confidence})"
            )

        result = self.router.route(intent, self.context)

        if result is None:
            self.logger.info("No intent matched, using conversational fallback")
            return self.nlg.generate_free_text(intent.raw)
            
        response = self.response_builder.build(intent, result)

        text = self.nlg.generate(response)

        self.logger.info(f"Skill result: {result}")
        return text
    

    def cli_loop(self):
        self.logger.info("CLI ready. Type 'exit' to quit.")

        while self.running:
            try:
                text = input("> ")

                if text.strip().lower() in ("exit", "quit"):
                    self.stop()
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