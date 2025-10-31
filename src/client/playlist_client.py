from src.business_object.playlist import Playlist
from src.dao.dao import DAO
from src.service.request_embedding_service import RequestEmbeddingService

class PlaylistClient:
    """
    Classe PlaylistClient
    Chaque méthode correspond à un endpoint de l'API
    """
    def instantiate_playlist(self, keyword, nbsongs):
        """
        Instancie un objet playlist à partir d'un mot-clé et d'un nombre de chanson.
        Fait appel à l'embedding service pour vectoriser le mot-clé et le comparer aux vecteurs paroles.

        Parameters
        ----------
        keyword : str
            le mot-clé à partir duquel instancier la playlist
        
        nbsong : int
            nombre maximal de chansons dans la playlist

        Returns
        ----------
        Playlist
            un objet playlist
        """
        #Extraction de tous les objets paroles de la BDD
        paroles = DAO.get_paroles()
        #Vectorisation du mot-clé
        key_vector = RequestEmbeddingService.vectorise(keyword)
        #Initialisation de la liste des distances
        compares = []
        #Calcul de la distance entre chacun des vecteurs paroles et le mot-clé
        for parole in paroles:
            compares.append([parole, RequestEmbeddingService.compare(key_vector, parole.vecteur)])
        #Tri de la liste des distances dans l'ordre décroissant
        compares.sort(key=lambda x: x[1], reverse=True)
        #Initialisation de la liste de chansons
        chansons = []
        #Si le nombre de chansons n'est pas supérieur au nombre de chansons dispos dans la BDD
        if not nbsongs > len(compares):
            #On ajoute les nbsongs premières chansons correspondant aux vecteurs de la liste des distances
            for i in range(nbsongs):
                chansons.append(DAO.get_chanson_from_paroles(compares[i][0]))
        #Sinon, on retourne une erreur
        else:
            raise Exception("Nombre de chanson demandé supérieur au nombre de chansons dans la BDD")
        #Retour de l'objet playlist avec les chansons
        return Playlist(keyword, chansons)
        
    def get_playlists(self):
        """
        Récupère et retourne la liste de toutes les playlists de la base de données

        Returns
        ----------
        list[Playlist]
            une liste de playlists
        """
        return DAO.get_playlists()
    
    def get_playlist(self, id):
        """
        Récupère une playlist à partir de son id

        Parameters
        ----------
        id : int
            l'id de la playlist à récupérer

        Returns
        ----------
        Playlist
            un objet playlist
        """
        return DAO.get_playlist_from_id(id)

    def get_playlist_chansons(self, id):
        """
        Récupère les chansons d'une playlist à partir de son id

        Parameters
        ----------
        id : int
            l'id de la playlist à partir de laquelle récupérer les chansons

        Returns
        ----------
        list[Chanson]
            une liste d'objets chansons
        """
        playlist = self.get_playlist_from_id(id)
        return playlist.get_chansons
