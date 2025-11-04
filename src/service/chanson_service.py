from service.parole_service import add_from_API

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from service.embedding_service import vectorise


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
