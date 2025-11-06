from dao.dao_chanson import DAO_chanson
from service.chanson_service import ChansonService


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
        new_chanson = ChansonService().instantiate_chanson(titre, artiste)
        try:
            # ChansonService().add_annee(new_chanson)
            ChansonService().add_chanson_paroles(new_chanson)
        except:
            return "La chanson n'est pas trouvable sur l'API"
        DAO_chanson().add_chanson(new_chanson)

    def get_chansons(self):
        """
        Récupère et retourne la liste de toutes les chansons de la base de données

        Returns
        ----------
        list[Chanson]
            une liste de chansons
        """
        return DAO_chanson().get_chansons()

    def get_chanson(self, titre, artiste):
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
        return DAO_chanson().get_chanson_from_titre_artiste(titre, artiste)

    def get_lyrics_by_titre_artiste(self, titre: str, artiste: str):
        """
        Récupère les paroles d'une chanson à partir de son titre et artiste.
        Formate la réponse pour le ParolesContentModel de l'API.
        """
        chanson = DAO_chanson().get_chanson_from_titre_artiste(titre, artiste)

        if chanson and chanson.paroles and chanson.paroles.content:
            return {
                "titre": chanson.titre,
                "artiste": chanson.artiste,
                "paroles": chanson.paroles.content,
            }

        return None
