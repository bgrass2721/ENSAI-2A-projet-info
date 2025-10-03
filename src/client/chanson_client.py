from src.business_object.chanson import Chanson
from src.business_object.paroles import Paroles
from src.dao.dao import DAO
from src.service.paroles_service import ParolesService


class ChansonClient:
    """
    Classe ChansonClient
    Chaque méthode correspond à un endpoint de l'API
    """

    def instantiate_chanson(self, titre, artiste):
        """
        Crée un objet chanson à partir d'un titre et d'un artiste

        Parameters
        ----------
        titre : str
            le titre de la chanson
        artiste : str
            le nom de l'artiste

        Returns
        ----------
        Chanson
            un objet chanson instancié avec le titre et l'artiste
        """
        return Chanson(titre, artiste)

    def get_chansons(self):
        """
        Récupère et retourne la liste de toutes les chansons de la base de données

        Returns
        ----------
        list[Chanson]
            une liste de chanson
        """
        return DAO.get_chansons()

    def get_chanson(self, id):
        """
        Récupère une chanson à partir de son id

        Parameters
        ----------
        id : int
            l'id de la chanson à récupérer

        Returns
        ----------
        Chanson
            un objet chanson
        """
        return DAO.get_chanson_from_id(id)

    def update_chanson(self, Chanson):
        """
        Modifie les informations d'une chanson dans la base de données
        Se sert de l'id et/ou des paroles pour savoir quelle chanson modifier.

        Parameters
        ----------
        Chanson
            la chanson avec les infos modifiées
        """
        DAO.update_chanson(Chanson)

    def add_chanson_paroles(self, chanson, paroles_content):
        """
        Permet d'ajouter manuellement les paroles d'une chanson
        Peut permettre aussi de modifier le contenu des paroles d'une chanson
        Remplace l'attribut paroles de chanson par un objet Paroles

        Parameters
        ----------
        chanson : Chanson
            l'objet chanson à modifier
        paroles_content : str
            le contenu des paroles
        """
        chanson.paroles = Paroles(paroles_content)

    def get_chanson_paroles(self, chanson):
        """
        Permet d'ajouter les paroles d'un chanson en allant les chercher sur une API
        Remplace l'attribut paroles de chanson par un objet Paroles

        Parameters
        ----------
        chanson : Chanson
            l'objet chanson à modifier
        """
        chanson.paroles = ParolesService.add_from_api(chanson)
