# 1) On part d'une image officielle Python (ici version 3.13 allégée "slim")
# 👉 Cela évite d’installer Python à la main : tout est déjà fourni par l’image.
FROM python:3.13-slim

# 2) Définir le dossier de travail à l'intérieur du container
# 👉 Tous les prochains RUN, COPY, CMD s’exécuteront dans ce dossier.
WORKDIR /app

# 3) Copier tout le projet dans l’image (dossier actuel -> /app)
# 👉 Le code, tests, requirements seront donc présents dans le container.
COPY . .

# 4) Mettre à jour pip + installer le package et les dépendances de dev
# - pip install -e . → installe ton projet en "mode editable"
# - pip install -r requirements-dev.txt → installe pytest, ruff, mypy
RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install -r requirements-dev.txt

# 5) Définir la commande par défaut du container
# 👉 Ici, on lance pytest avec couverture, donc à chaque "docker run freshcart"
#    les tests s’exécutent automatiquement.
CMD ["pytest", "--cov=src/freshcart", "--cov-report=term-missing"]
