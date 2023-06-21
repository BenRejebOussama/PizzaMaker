# PizzaMaker
DRF test project
# Django REST Framework Example

Ce projet est un exemple simple de création d'une API REST avec Django et Django REST Framework (DRF). Il fournit des endpoints pour gérer des objets "Pizza" et leurs ingrédients associés.

## Installation

1. Clonez le référentiel :

git clone https://github.com/BenRejebOussama/PizzaMaker.git


2. Accédez au répertoire du projet :

cd PizzaMaker


3. Créez et activez un environnement virtuel :

python3 -m venv env
source env/bin/activate


4. Installez les dépendances du projet :

pip install -r requirements.txt


5. Lancez le serveur de développement :

python manage.py runserver


6. Accédez à l'application dans votre navigateur à l'adresse [http://localhost:8000/](http://localhost:8000/).

## Endpoints API

L'API fournit les endpoints suivants :

- `GET /pizza/` : Récupère la liste de toutes les pizzas.
- `GET /pizza/{id}/` : Récupère les détails d'une pizza spécifique.
- `POST /pizza/` : Crée une nouvelle pizza.
- `PUT /pizza/{id}/` : Met à jour une pizza existante.
- `DELETE /pizza/{id}/` : Supprime une pizza spécifique.
- `GET /ingredients/` : Récupère la liste de tous les ingrédients.
- `GET /ingredients/{id}/` : Récupère les détails d'un ingrédient spécifique.
- `POST /ingredients/` : Crée un nouvel ingrédient.
- `PUT /ingredients/{id}/` : Met à jour un ingrédient existant.
- `DELETE /ingredients/{id}/` : Supprime un ingrédient spécifique.

## Exemples d'utilisation

Voici quelques exemples d'utilisation de l'API avec cURL :

1. Récupérer la liste de toutes les pizzas :
curl -X GET http://localhost:8000/pizza/


2. Créer une nouvelle pizza :

curl -X POST -H "Content-Type: application/json" -d '{"name": "Pizza Margherita", "price": 10.99}' http://localhost:8000/pizza/


3. Mettre à jour une pizza existante :

curl -X PUT -H "Content-Type: application/json" -d '{"name": "Pizza Margherita", "price": 12.99}' http://localhost:8000/pizza/{id}/


N'hésitez pas à explorer davantage les fonctionnalités de l'API en utilisant les endpoints fournis.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez contribuer à ce projet, veuillez ouvrir une nouvelle demande de pull (pull request) avec vos modifications.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.


