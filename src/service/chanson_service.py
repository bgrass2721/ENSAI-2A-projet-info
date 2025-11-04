from service.parole_service import add_from_API

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from dao.dao import DAO
from service.embedding_service import vectorise


class chanson_service:
    def instantiate_chanson(titre: str, artiste: str, annee: int = None) -> None:
        # création de l'objet Chanson
        chanson = Chanson(titre, artiste)
        # Ajout du vec paroles
        paroles_str = add_from_API(chanson)
        paroles_vecteur = vectorise(paroles_str)
        chanson.paroles = Paroles(content=paroles_str, vecteur=paroles_vecteur)
        # Ajout de la chanson à la DB
        DAO.add_chanson(chanson=chanson)
