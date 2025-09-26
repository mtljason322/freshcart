# 🛒 FreshCart

Projet d’entraînement **Python + DevOps**

## 🎯 Objectifs

- Python “propre” : OOP, tests, packaging, async, API.
- Outils DevOps :
  - Git/GitHub
  - CI/CD (GitHub Actions)
  - Docker
  - Terraform + AWS Free Tier
  - Qualité (SonarQube)
  - Sécurité (Snyk)
  - Ansible, etc.

## ⚡ Lancement rapide (sanity check)

Après avoir cloné le dépôt et activé votre venv (voir plus bas) :

python hello.py

## 🗂️ Sommaire

- Pré-requis
- Installation rapide
- Commandes utiles
- API Utilisateur
- Product
- PerishableProduct
- Inventory
- Qualité & CI
- Structure
- Dépannage

## 🔧 Pré-requis

- Python 3.11+ (idéal : 3.13)
- Git
- Windows (PowerShell/CMD) ou macOS/Linux (Terminal)

## 🚀 Installation rapide

### 1) Cloner le dépôt

git clone <URL_DU_REPO> && cd freshcart

### 2) Créer/activer l’environnement virtuel

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows CMD
python -m venv .venv
.\.venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

### 3) Installer le package en mode développement (editable)

pip install -e .

# Pour quitter le venv :
deactivate

## 🛠️ Commandes utiles

# ✅ Tests unitaires avec couverture
pytest --cov=src/freshcart --cov-report=term-missing

# 🎨 Lint & format (Ruff)
ruff check src tests --fix

# 🔍 Typage statique (MyPy)
mypy src

## 📦 API Utilisateur

Le package s’importe sous le nom `freshcart`.
Les classes principales sont exposées à la racine pour des imports courts.

# --- Product ---
from freshcart import Product

# 3e argument positionnel = prix initial
p = Product("SKU001", "Café", 8.0)

# ou en nommé (InitVar "initial_price")
p = Product(sku="SKU001", name="Café", initial_price=8.0)

p.price            # -> 8.0 (propriété avec validation + arrondi)
p.final_price()    # -> 8.0 (polymorphisme, peut être surchargé)
print(p)           # "Café (SKU001) - 8.00$"

# --- PerishableProduct ---
from freshcart import PerishableProduct
from datetime import date, timedelta

lait = PerishableProduct(
    "SKU002", "Lait", 4.0,
    expiry_date=date.today() + timedelta(days=2)  # paramètre keyword-only
)

lait.is_expired      # -> False (aujourd'hui < date d'expiration)
lait.final_price()   # -> 2.0 (remise -50% si <= 3 jours avant expiration)

# --- Inventory ---
from freshcart import Inventory, Product

inv = Inventory()
inv.add(Product("SKU001", "Café", 8.0))
inv.add(Product("SKU003", "Sucre", 2.0))

inv.all()           # -> liste des produits
inv.expired()       # -> liste des périmés (si périssables)
inv.total_value()   # -> somme des final_price() (polymorphisme)

## ✅ Qualité & CI

- Tests : Pytest + couverture.
- Lint : Ruff (PEP 8, ordre d’imports, lignes longues, etc.).
- Types : MyPy (Protocol/Duck typing, InitVar, annotations).

# ⚙️ CI GitHub Actions
- .github/workflows/tests.yml → exécute Pytest
- .github/workflows/lint.yml → exécute Ruff + MyPy

> La CI échoue si le linting, le typing ou les tests échouent → protège la branche `main`.

## 📁 Structure

freshcart/
  src/freshcart/
    __init__.py               # expose Product, PerishableProduct, Inventory
    domain/
      products.py             # Product, PerishableProduct (+ Pricable/Protocol)
      inventory.py            # Inventory, exception métier, décorateur log_call
  tests/                      # tests unitaires (couverture élevée)
  hello.py                    # sanity check simple (installation Python)

## 🧯 Dépannage

# ❌ ModuleNotFoundError: freshcart
# Assurez-vous d’avoir bien activé l’environnement et installé le package :

pip install -e .

# ❌ NameError: name 'date' is not defined
# Pensez à importer :

from datetime import date, timedelta

# ⚠️ Ruff signale I001 (imports non triés) ou E501 (lignes > 88 cols)
ruff check src tests --fix

# ⚠️ Vérification de type
mypy src

## 🐳 Docker

### Construire l’image

# Depuis la racine du projet :
docker build -t freshcart .

### Lancer les tests dans le container

# Le Dockerfile définit :
# CMD ["pytest", "--cov=src/freshcart", "--cov-report=term-missing"]
docker run --rm freshcart

### Exécuter d’autres commandes dans le container

# 🔍 Lancer Ruff dans le container
docker run --rm freshcart ruff check src tests

# 📐 Lancer MyPy dans le container
docker run --rm freshcart mypy src

# ▶️ Exécuter un script d’exemple
docker run --rm freshcart python examples/demo_inventory.py

### 🚀 Démarrer une API (plus tard)

# Nous ajouterons une API (FastAPI) dans une prochaine étape. Pour l’exposer :
docker run --rm -p 8000:8000 freshcart uvicorn freshcart.api.main:app --host 0.0.0.0 --port 8000

### ✅ Commit (branche dédiée doc)

git checkout -b docs/readme-docker
git add README.md
git commit -m "docs: add Docker usage section (build, run, override CMD)"
git push -u origin docs/readme-docker

### 📄 PR (texte court)

What: Add Docker section in README (build/run/override CMD)  
Why: Provide reproducible environment guidance  
How to test: docker build -t freshcart . && docker run --rm freshcart  
Notes: No code changes


