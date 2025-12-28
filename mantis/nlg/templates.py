import random


class TemplatesNLG:
    def generate(
        self,
        response=None,
        user_text: str | None = None,
        introduce: bool = False
    ) -> str:
        intro = "Bonjour, je suis Mantis. " if introduce else ""

        # Skill response (unified)
        if response is not None and response.type == "skill":

            # ---- SYSTEM ----
            if response.skill == "system":
                user = response.data.get("user", "inconnu")
                status = response.data.get("status", "unknown")

                base = random.choice([
                    f"Le système fonctionne correctement. Utilisateur actif : {user}.",
                    f"Tout est opérationnel. Connecté en tant que {user}.",
                    f"Le système est en marche. Utilisateur courant : {user}.",
                ])
                return intro + base

            # ---- WEATHER ----
            if response.skill == "weather":
                data = response.data
                location = data.get("location", "unknown")

                if location == "unknown":
                    return intro + "Pour vous donner la météo, j’ai besoin de connaître la ville."

                return intro + (
                    f"(Simulation) À {location}, il fait actuellement "
                    f"{data.get('temperature')}°C avec un temps {data.get('condition')}."
                )

            # ---- UNKNOWN SKILL ----
            return intro + "Cette action a été exécutée."

        # Fallback (no response)
        return intro + "Je ne sais pas encore répondre à cette demande."