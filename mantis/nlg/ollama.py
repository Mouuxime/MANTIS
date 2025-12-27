import ollama


class OllamaNLG:
    def __init__(self, model: str = "mistral"):
        self.model = model

    def generate(
        self,
        response=None,
        user_text: str | None = None,
        introduce: bool = False
    ) -> str:
        """
        Génère une réponse naturelle.
        - response : objet Response (si issu d'un skill)
        - user_text : texte brut utilisateur (fallback conversationnel)
        - introduce : indique si Mantis doit se présenter
        """

        # 🔹 Instructions système de base
        system_prompt = (
            "Tu es Mantis, une IA locale.\n"
            "Tu réponds en français, de manière naturelle et concise.\n"
            "Tu utilises vous pour t'adresser à l'utilisateur.\n"
            "Tu parles à la première personne.\n"
        )

        # 🔹 Présentation contrôlée par le Kernel
        if introduce:
            system_prompt += (
                "Présente-toi en disant explicitement : 'Bonjour, je suis Mantis'. Fais-le UNE SEULE FOIS.\n"
            )
        else:
            system_prompt += (
                "Ne te présente PAS.\n"
                "Ne dis PAS ton nom\n"
                "Ne dis PAS Bonjour ou Salut\n"
                "Réponds directement à la demande\n"
            )

        # 🔹 Construction du prompt
        if response is not None:
            prompt = (
                system_prompt
                + "\nType de réponse : "
                + str(response.type)
                + "\nDonnées : "
                + str(response.data)
                + "\nRéponse :"
            )
        else:
            prompt = (
                system_prompt
                + "\nUtilisateur : "
                + str(user_text)
                + "\nMantis :"
            )

        result = ollama.generate(
            model=self.model,
            prompt=prompt
        )

        return result["response"].strip()
