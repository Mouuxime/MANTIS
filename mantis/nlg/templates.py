import random

class TemplatesNLG:
    def generate(self, response) -> str:
        if response.type == "system_status":
            user = response.data.get("user", "inconnu")
            return random.choice([
                f"Le système fonctionne correctement. Utilisateur actif : {user}.",
                f"Tout est opérationnel. Connecté en tant que {user}.",
                f"Le système est en marche. Utilisateur courant : {user}."
            ])

        return "C’est fait."
