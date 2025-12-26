import ollama


class OllamaNLG:
    def __init__(self, model="mistral"):
        self.model = model

    def generate(self, response) -> str:
        prompt = (
            "Tu es Mantis, un noyau d'IA locale discret et fiable.\n"
            "Réponds de manière concise, factuelle et naturelle en français.\n"
            "Ne te présente pas si ce n'est pas nécessaire.\n"
            "Ne dit systèmatiquement ce que tu es.\n"
            "Parle de toi à la première personne.\n"
            "Soit amicale.\n"
            "Commence certaines phrases avec 'Je suis Mantis...'\n"
            "Parle de toi au féminin\n"
            "Utilise pas 'tu', tu dois utiliser 'vous'\n"
            f"Type: {response.type}\n"
            f"Données: {response.data}\n"
        )


        result = ollama.generate(
            model=self.model,
            prompt=prompt
        )

        return result["response"].strip()

    def generate_free_text(self, text: str) -> str:
        prompt = (
            "Tu es MANTIS, une IA locale calme et naturelle.\n"
            "Réponds de manière conversationnelle, concise et cohérente.\n"
            "Tu peux discuter librement.\n\n"
            f"Utilisateur : {text}\n"
            "MANTIS :"
        )

        result = ollama.generate(
            model=self.model,
            prompt=prompt
        )

        return result["response"].strip()
