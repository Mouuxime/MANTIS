import random


class TemplatesNLG:
    def generate(
        self,
        response=None,
        user_text: str | None = None,
        introduce: bool = False
    ) -> str:
        intro = ""
        if introduce:
            intro = "Bonjour, je suis Mantis. "

        # 🔹 Réponse issue d'un skill
        if response is not None:
            if response.type == "system_status":
                user = response.data.get("user", "inconnu")
                base = random.choice([
                    f"Le système fonctionne correctement. Utilisateur actif : {user}.",
                    f"Tout est opérationnel. Connecté en tant que {user}.",
                    f"Le système est en marche. Utilisateur courant : {user}."
                ])
            else:
                base = "C'est fait."

            return intro + base

        # 🔹 Fallback conversationnel
        base = "Je ne sais pas encore répondre à cette demande."
        return intro + base
