from dao.dao_playlist import DAO_playlist
from service.playlist_service import PlaylistService


class PlaylistClient:
    """
    Classe PlaylistClient
    Chaque méthode correspond à un endpoint de l'API
    """

    def request_playlist(self, keyword, nbsongs):
        """
        Fait appel à la fonction instantiate_playlist du service layer pour créer une nouvelle
        playlist à partir d'un mot-clé et d'un nombre de chansons.
        """
        new_playlist = PlaylistService.instantiate_playlist(keyword, nbsongs)
        DAO_playlist().add_playlist(new_playlist)
        return new_playlist.afficher()

    def get_playlists(self):
        """
        Récupère et retourne la liste de toutes les playlists de la base de données

        Returns
        ----------
        list[Playlist]
            une liste de playlists
        """
        return DAO_playlist().get_playlists()

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
        return DAO_playlist().get_playlist_from_id(id)

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
        playlist = DAO_playlist().get_playlist_from_id(id)
        return playlist.get_chansons
