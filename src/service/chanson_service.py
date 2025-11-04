import requests

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from service.embedding_service import vectorise
from service.parole_service import add_from_API


class chanson_service:
    def instantiate_chanson(titre: str, artiste: str, annee: int = None) -> Chanson:
        """
        Création de l'objet Chanson
        """
        chanson = Chanson(titre, artiste)
        return chanson

    def add_chanson_paroles(chanson: Chanson) -> None:
        """
        Ajout du vec paroles
        """
        paroles_str = add_from_API(chanson)
        paroles_vecteur = vectorise(paroles_str)
        chanson.paroles = Paroles(content=paroles_str, vecteur=paroles_vecteur)

    def add_annee(chanson: Chanson):
        """
        Recherche l'année de sortie d'une chanson via LRCLIB à partir du titre et de l'artiste.
        Retourne l'année si trouvée, sinon None.
        """
        # URL de l'API de recherche LRCLIB
        url = "https://lrclib.net/api/get"

        # Paramètres de la requête
        params = {"track_name": chanson.titre, "artist_name": chanson.artiste}
        params = {"track_name": chanson.titre, "artist_name": chanson.artiste}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extraire l'année si disponible
            annee = data.get("year")  # Ici, "year" est une supposition, adapte cela si nécessaire.
            chanson.annee = annee

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la requête : {e}")
