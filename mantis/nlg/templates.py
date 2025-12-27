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

        #Skill response
        if response is not None:

            print("\n[DEBUG][TemplatesNLG] response =", response)
            print("[DEBUG][TemplatesNLG] type(response) =", type(response))

            if not isinstance(response, dict):
                print("[DEBUG][TemplatesNLG] dir(response) =", dir (response))

            if isinstance(response, dict):
                print("[DEBUG][TemplatesNLG] response.keys() =", response.keys())

            #---System status---
            if response.type == "system_status":
                user = response.data.get("user", "inconnu")
                base = random.choice([
                    f"Le système fonctionne correctement. Utilisateur actif : {user}.",
                    f"Tout est opérationnel. Connecté en tant que {user}.",
                    f"Le système est en marche. Utilisateur courant : {user}."
                ])
                return intro + base
            
            #---Weather---
            if response.type == "weather":
                data = response.data
                location = data.get("location", "unknown")

                if location == "unknown":
                    return intro + "Pour vous donner la météo, j'ai besoin de connaître la ville."
                
                return intro + (
                    f"(Simulation) A {location}, il fait actuellement"
                    f"{data.get('temperature')}°C avec un temps {data.get('condition')}"
                )
            
            return intro + "Cette action a été exécutée."

        #Fallback
        base = "Je ne sais pas encore répondre à cette demande."
        return intro + base
