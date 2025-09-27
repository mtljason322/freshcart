"""
Point d’entrée de l’API.

FC-3 (placeholder) :
- On ne dépend PAS encore de FastAPI ici (pour que le projet reste installable
  même si tu n’as pas encore ajouté les dépendances).
- En FC-4, on ajoutera `from fastapi import FastAPI` + une factory `create_app()`.
- En FC-5, on branchera les routes (health, products, inventory...).
"""

def create_app_placeholder() -> None:
    """Petite fonction temporaire pour valider l’import du module en FC-3.
    Remplacée par `create_app()` (FastAPI) en FC-4.
    """
    return None


if __name__ == "__main__":
    # Note dev : en FC-6 on lancera uvicorn ici.
    print("FreshCart API skeleton ready.")
