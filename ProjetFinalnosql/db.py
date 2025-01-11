from pymongo import MongoClient


class MongoDBDatabase:
    def __init__(self, uri: str, database_name: str):
        """
        Initialise une connexion à MongoDB.

        :param uri: URI de connexion MongoDB (ex: "mongodb://localhost:27017").
        :param database_name: Nom de la base de données.
        """
        try:
            self.client = MongoClient(uri)
            self.database = self.client[database_name]
            print(f"Connecté à la base de données: {database_name}")
        except ConnectionError as e:
            print(f"Erreur de connexion à MongoDB : {e}")
            self.client = None
            self.database = None


    def get_collection(self, collection_name: str):
        """
        Récupère une collection de la base de données.

        :param collection_name: Nom de la collection.
        :return: Collection MongoDB.
        """
        if self.database is not None:
            return self.database[collection_name]
        else:
            print("La base de données n'est pas initialisée.")
            return None

    def insert_one(self, collection_name: str, document: dict):
        """
        Insère un document dans une collection.

        :param collection_name: Nom de la collection.
        :param document: Document à insérer (dict).
        :return: ID du document inséré.
        """
        try:
            collection = self.get_collection(collection_name)
            if collection:
                result = collection.insert_one(document)
                return result.inserted_id
        except:
            print(f"Erreur lors de l'insertion")
        return None




    def find(self, collection_name: str, query: dict = {}):
        """
        Récupère des documents correspondant à une requête.

        :param collection_name: Nom de la collection.
        :param query: Requête MongoDB (dict).
        :return: Liste des documents correspondants.
        """
        try:
            collection = self.get_collection(collection_name)
            if collection:
                return list(collection.find(query))
        except:
            print(f"Erreur lors de la récupération")
        return []

    def update_one(self, collection_name: str, query: dict, update: dict):
        """
        Met à jour un document correspondant à une requête.

        :param collection_name: Nom de la collection.
        :param query: Requête MongoDB (dict).
        :param update: Mise à jour à appliquer (dict).
        :return: Résultat de l'opération.
        """
        try:
            collection = self.get_collection(collection_name)
            if collection:
                return collection.update_one(query, {"$set": update})
        except:
            print(f"Erreur lors de la mise à jour")
        return None

    def delete_one(self, collection_name: str, query: dict):
        """
        Supprime un document correspondant à une requête.

        :param collection_name: Nom de la collection.
        :param query: Requête MongoDB (dict).
        :return: Résultat de l'opération.
        """
        try:
            collection = self.get_collection(collection_name)
            if collection:
                return collection.delete_one(query)
        except:
            print(f"Erreur lors de la suppression")
        return None

    def close(self):
        """
        Ferme la connexion au client MongoDB.
        """
        if self.client:
            self.client.close()
            print("Connexion MongoDB fermée.")
