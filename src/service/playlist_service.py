from business_object.chanson import Chanson
from business_object.playlist import Playlist
from dao.dao_chanson import DAO_chanson
from dao.dao_paroles import DAO_paroles
from service.request_embedding_service import RequestEmbeddingService


class PlaylistService:
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
        # Extraction de tous les objets paroles de la BDD
        paroles = DAO_paroles().get_paroles()
        # Vectorisation du mot-clé
        key_vector = RequestEmbeddingService().vectorise(keyword)
        # Initialisation de la liste des distances
        compares = []
        # Si la DAO a pu récupérer les paroles
        if paroles:
            # Calcul de la distance entre chacun des vecteurs paroles et le mot-clé
            for parole in paroles:
                compares.append([parole, RequestEmbeddingService().compare(key_vector, parole.vecteur)])
        # Sinon
        else:
            # Il n'y a pas de chansons dans la base de données
            raise Exception("Il n'y a pas de chansons dans la base de données")
        # Tri de la liste des distances dans l'ordre décroissant
        compares.sort(key=lambda x: x[1], reverse=True)
        # Initialisation de la liste de chansons
        chansons = []
        # Si le nombre de chansons n'est pas supérieur au nombre de chansons dispos dans la BDD
        if not nbsongs > len(compares):
            # On ajoute les nbsongs premières chansons correspondant aux vecteurs de la liste des distances
            for i in range(nbsongs):
                chansons.append(
                    DAO_chanson().get_chanson_from_embed_paroles(compares[i][0].vecteur)
                )
        # Sinon, on ajoute toutes les chansons dans l'ordre
        else:
            for compare in compares:
                chansons.append(
                    DAO_chanson().get_chanson_from_from_embed_paroles(compare[0].vecteur)
                )
        # Retour de l'objet playlist avec les chansons
        return Playlist(keyword, chansons)

    def add_chanson(self, playlist: Playlist, chanson: Chanson) -> bool:
        """
        Ajoute une chanson à une playlist.

        Args:
            playlist: L'objet Playlist
            chanson: L'objet Chanson à ajouter

        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        if chanson not in playlist.chansons:
            playlist.chansons.append(chanson)

    def del_chanson(self, playlist: Playlist, chanson: Chanson) -> bool:
        """
        Supprime une chanson d'une playlist.

        Args:
            playlist: L'objet Playlist
            chanson: L'objet Chanson à supprimer

        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        if chanson in playlist.chansons:
            playlist.chansons.remove(chanson)


if __name__ == "__main__":
    PlaylistService().instantiate_playlist("amour", 10)
