import json
from pymongo import MongoClient

db = MongoClient().get_database("base_formulaires")
collection = db["Formulaires"]

file_data = [
    {
        "_id": {"$oid": "679c8c90fa994a9a5df38b7f"},
        "nom": "Quiz de culture générale",
        "description": "Un quiz pour tester vos connaissances générales.",
        "password": "quiz123",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b7c"},
                "intitule": "Quelle est la capitale de la France ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b7d"},
                "intitule": "Quels sont les continents de la planète Terre ?",
                "type": "multiple",
                "reponses": [
                    "Europe",
                    "Asie",
                    "Afrique",
                    "Amérique du Sud",
                    "Amérique du Nord",
                    "Antarctique",
                    "Océanie"
                ]
            }
        ]
    },
    {
        "_id": {"$oid": "679c8c90fa994a9a5df38b80"},
        "nom": "Quiz sur l'espace",
        "description": "Testez vos connaissances sur l'univers et l'astronomie.",
        "password": "spaceX",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b81"},
                "intitule": "Quelle est la planète la plus proche du Soleil ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b82"},
                "intitule": "Quelles planètes du système solaire ont des anneaux ?",
                "type": "multiple",
                "reponses": [
                    "Saturne",
                    "Jupiter",
                    "Uranus",
                    "Neptune"
                ]
            }
        ]
    }, {
        "_id": {"$oid": "679c8c90fa994a9a5df38b83"},
        "nom": "Quiz Histoire",
        "description": "Testez vos connaissances sur les événements historiques marquants.",
        "password": "histoire2024",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b84"},
                "intitule": "En quelle année la Révolution française a-t-elle commencé ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b85"},
                "intitule": "Quels pays faisaient partie des Alliés pendant la Seconde Guerre mondiale ?",
                "type": "multiple",
                "reponses": [
                    "France",
                    "Royaume-Uni",
                    "États-Unis",
                    "URSS",
                    "Chine"
                ]
            }
        ]
    },
    {
        "_id": {"$oid": "679c8c90fa994a9a5df38b86"},
        "nom": "Quiz Sciences",
        "description": "Un quiz pour les passionnés de sciences naturelles et physiques.",
        "password": "science123",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b87"},
                "intitule": "Quel est l’élément chimique le plus abondant dans l’univers ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b88"},
                "intitule": "Quels sont les états physiques de la matière ?",
                "type": "multiple",
                "reponses": [
                     "Solide",
                     "Liquide",
                     "Gazeux",
                     "Plasma"
                ]
            }
        ]
    },
    {
        "_id": {"$oid": "679c8c90fa994a9a5df38b89"},
        "nom": "Quiz Cinéma",
        "description": "Testez vos connaissances sur le monde du cinéma.",
        "password": "cinefan",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b8a"},
                "intitule": "Quel réalisateur a créé le film 'Inception' ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b8b"},
                "intitule": "Quels films ont remporté un Oscar du meilleur film ?",
                "type": "multiple",
                "reponses": [
                     "Titanic",
                     "Forrest Gump",
                     "Parasite",
                     "Gladiator",
                     "Le Seigneur des Anneaux : Le Retour du Roi"
                ]
            }
        ]
    },
    {
        "_id": {"$oid": "679c8c90fa994a9a5df38b8c"},
        "nom": "Quiz Sport",
        "description": "Un quiz pour les amateurs de sport.",
        "password": "sportquiz",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b8d"},
                "intitule": "Dans quel sport utilise-t-on une raquette et un volant ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b8e"},
                "intitule": "Quels pays ont remporté la Coupe du Monde de football ?",
                "type": "multiple",
                "reponses": [
                    "Brésil",
                    "Allemagne",
                    "Italie",
                    "Argentine",
                    "France"]
            }
        ]
    },
    {
        "_id": {"$oid": "679c8c90fa994a9a5df38b8f"},
        "nom": "Quiz Musique",
        "description": "Testez vos connaissances sur l'univers musical.",
        "password": "melomanes",
        "Questions": [
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b90"},
                "intitule": "Quel artiste a chanté 'Thriller' ?",
                "type": "unique"
            },
            {
                "_id": {"$oid": "679c8c90fa994a9a5df38b91"},
                "intitule": "Quels instruments font partie d'un orchestre classique ?",
                "type": "multiple",
                "reponses": [
                    "Violon",
                    "Piano",
                    "Trompette",
                    "Flûte",
                    "Contrebasse"
                ]
            }
        ]
    }
]

from bson import ObjectId

for doc in file_data:
    doc["_id"] = ObjectId(doc["_id"]["$oid"])
    for question in doc["Questions"]:
        question["_id"] = ObjectId(question["_id"]["$oid"])

# Insérer dans MongoDB
collection.insert_many(file_data)

print("✅ Données insérées avec succès !")
