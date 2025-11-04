from business_object.chanson import Chanson
from business_object.paroles import Paroles
from business_object.playlist import Playlist
from dao.dao import DAO
from dao.db_connection import DBConnection


class DAO_playlist(DAO):
    def add_playlist(self, playlist: Playlist) -> None:
        """
        Ajoute une playlist à la table PLAYLIST de la BD et remplit la table CATALOGUE de la BD
        """
        nom = playlist.nom
        chansons = playlist.chansons
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO PLAYLIST (nom)
                    VALUES (%s)
                    RETURNING id_playlist;
                    """,
                    (nom,),
                )
                id_playlist = cursor.fetchone()[0]  # (id, )
                for chanson in chansons:
                    embed_paroles = chanson.paroles.vecteur
                    cursor.execute(
                        """
                        INSERT INTO CATALOGUE (id_playlist, embed_paroles)
                        VALUES (%s, %s);
                        """,
                        (id_playlist, embed_paroles),
                    )
                connection.commit()

    def get_playlists(self) -> list[Playlist]:
        """
        Liste tous les objets Playlist des playlists enregistrés dans la BD
        """
        playlists = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # récupération de l'identifiant de chaque playlist
                cursor.execute(
                    """
                    SELECT id_playlist, nom from PLAYLIST;
                    """
                )  # [(id, nom), (id, nom), ...]
                tup_playlists = cursor.fetchall()  # [(id, nom), (id, nom), ...]
                # récupération des chansons de chaque playlist
                for id_playlist, nom in tup_playlists:
                    cursor.execute(
                        """
                        SELECT cat.nom, c.embed_paroles, c.titre, c.artiste, c.annee, c.str_paroles
                        FROM CHANSON c
                        JOIN CATALOGUE cat ON c.embed_paroles = cat.embed_paroles
                        WHERE cat.id_playlist = %s;
                        """,
                        (id_playlist,),
                    )
                    tup_chansons = cursor.fetchall()
                    # création liste d'objets Chanson
                    chansons = []
                    for embed_paroles, titre, artiste, annee, str_paroles in tup_chansons:
                        paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
                        chanson = Chanson(titre, artiste, annee, paroles)
                        chansons.append(chanson)
                    # création objet Playlist
                    playlist = Playlist(nom, chansons)
                    # ajout de la playlist à la liste des playlists
                    playlists.append(playlist)
            return playlists

    def get_playlist_from_id(self, id: int) -> Playlist | None:
        """
        Liste tous les objets Playlist des playlists enregistrés dans la BD
        """
        playlists = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # récupération de l'identifiant de chaque playlist
                cursor.execute(
                    """
                    SELECT id_playlist, nom from PLAYLIST
                    WHERE id_playlist = %s;
                    """,
                    (id,),
                )  # [(id, nom), (id, nom), ...] avec toujours le même id
                tup_playlists = cursor.fetchall()
                # récupération des chansons de chaque playlist
                for id_playlist, nom in tup_playlists:
                    cursor.execute(
                        """
                        SELECT cat.nom, c.embed_paroles, c.titre, c.artiste, c.annee, c.str_paroles
                        FROM CHANSON c
                        JOIN CATALOGUE cat ON c.embed_paroles = cat.embed_paroles
                        WHERE cat.id_playlist = %s;
                        """,
                        (id_playlist,),
                    )
                    tup_chansons = cursor.fetchall()
                    # création liste d'objets Chanson
                    chansons = []
                    for embed_paroles, titre, artiste, annee, str_paroles in tup_chansons:
                        paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
                        chanson = Chanson(titre, artiste, annee, paroles)
                        chansons.append(chanson)
                    # création objet Playlist
                    playlist = Playlist(nom, chansons)
                    # ajout de la playlist à la liste des playlists
                    playlists.append(playlist)
            return playlists
