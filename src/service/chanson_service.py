import requests

from business_object.chanson import Chanson
from service.paroles_embedding_service import ParolesEmbeddingService
from service.paroles_service import ParolesService


class ChansonService:
    def instantiate_chanson(self, titre: str, artiste: str) -> Chanson:
        """
        Création de l'objet Chanson
        """
        chanson = Chanson(titre, artiste)
        return chanson

    def add_chanson_paroles(self, chanson: Chanson) -> None:
        """
        Ajout du vec paroles
        """
        paroles = ParolesService().add_from_API(chanson)
        paroles.vecteur = ParolesEmbeddingService().vectorise(paroles.content)
        chanson.paroles = paroles

    # def add_annee(self, chanson: Chanson):
    #     """
    #     Recherche l'année de sortie d'une chanson via LRCLIB à partir du titre et de l'artiste.
    #     Retourne l'année si trouvée, sinon None.
    #     """
    #     # URL de l'API de recherche LRCLIB
    #     url = "https://lrclib.net/api/get"

    #     # Paramètres de la requête
    #     params = {"track_name": chanson.titre, "artist_name": chanson.artiste}

    #     try:
    #         response = requests.get(url, params=params, timeout=10)
    #         response.raise_for_status()
    #         data = response.json()

    #         # Extraire l'année si disponible
    #         annee = data.get("year")  # Ici, "year" est une supposition, adapte cela si nécessaire.
    #         chanson.annee = annee

    #     except requests.exceptions.RequestException as e:
    #         raise Exception(f"Erreur lors de la requête : {e}")


if __name__ == "__main__":
    chanson = ChansonService().instantiate_chanson("Imagine", "John Lennon")
    ChansonService().add_chanson_paroles(chanson)
    print(chanson.paroles)
