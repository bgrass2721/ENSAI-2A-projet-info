from business_object.paroles import Paroles
from dao.dao import DAO
from service.chanson_service import ChansonService
from service.paroles_service import ParolesService


class ChansonClient:
    """
    Classe ChansonClient
    Chaque méthode correspond à un endpoint de l'API
    """

    def add_new_chanson(self, titre, artiste):
        """
        Permet à l'utilisateur d'ajouter une nouvelle chanson dans la database.
        Ajoute automatiquement l'année de sortie et les paroles à partir du service chanson.

        Parameters
        ----------
        titre : str
            le titre de la chanson
        artiste : str
            le nom de l'artiste

        Returns
        ----------
        str
            Message de validation / d'erreur
        """
        new_chanson = ChansonService.instantiate_chanson(titre, artiste)
        try:
            ChansonService.add_annee(new_chanson)
            ChansonService.add_chanson_paroles(new_chanson)
        except:
            return "La chanson n'est pas trouvable sur l'API"
        DAO.add_chanson(new_chanson)

    def get_chansons(self):
        """
        Récupère et retourne la liste de toutes les chansons de la base de données

        Returns
        ----------
        list[Chanson]
            une liste de chansons
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
