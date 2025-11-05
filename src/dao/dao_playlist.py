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
                    RETURNING id_playlist
                    ON CONFLICT DO NOTHING;
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
                # Récupération de l'identifiant et du nom de chaque playlist
                cursor.execute(
                    """
                    SELECT id_playlist, nom from PLAYLIST;
                    """
                )  # [(id, nom), (id, nom), ...]
                tup_playlists = cursor.fetchall()
                for id_playlist, nom in tup_playlists:
                    # Récupération des chansons de chaque playlist
                    cursor.execute(
                        """
                        SELECT c.embed_paroles, c.titre, c.artiste, c.annee, c.str_paroles
                        FROM CHANSON c
                        JOIN CATALOGUE cat ON c.embed_paroles = cat.embed_paroles
                        WHERE cat.id_playlist = %s;
                        """,
                        (id_playlist,),
                    )  # [(nom, embed_paroles, titre, artiste, annee, str_paroles), (...), ...]
                    tup_chansons = cursor.fetchall()
                    chansons = []
                    for embed_paroles, titre, artiste, annee, str_paroles in tup_chansons:
                        paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
                        # Création objet Chanson
                        chanson = Chanson(titre, artiste, annee, paroles)
                        # Ajout de la chanson à liste de chansons
                        chansons.append(chanson)
                    # Création objet Playlist
                    playlist = Playlist(nom, chansons)
                    # Ajout de la playlist à la liste des playlists
                    playlists.append(playlist)
        return playlists

    def get_playlist_from_id(self, id_playlist: int) -> Playlist | None:
        """
        Liste tous les objets Playlist des playlists enregistrés dans la BD
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Récupération des chansons et du nom de la playlist
                cursor.execute(
                    """
                    SELECT cat.nom, c.embed_paroles, c.titre, c.artiste, c.annee, c.str_paroles
                    FROM CHANSON c
                    JOIN CATALOGUE cat ON c.embed_paroles = cat.embed_paroles
                    WHERE cat.id_playlist = %s;
                    """,
                    (id_playlist,),
                )  # [(nom, embed_paroles, titre, artiste, annee, str_paroles), (...), ...]
                res = cursor.fetchall()
                chansons = []
                for _, embed_paroles, titre, artiste, annee, str_paroles in res:
                    paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
                    # Création objet Chanson
                    chanson = Chanson(titre, artiste, annee, paroles)
                    # Ajout de la chanson à liste de chansons
                    chansons.append(chanson)
                    # Création objet Playlist
                nom = res[0][0]
                playlist = Playlist(nom, chansons)
                return playlist
        return None

    def del_playlist_via_id(self, id_playlist: int) -> None:
        """
        Supprime une playlist de la table PLAYLIST via son id
        Les lignes associées dans CATALOGUE sont supprimées
        automatiquement grâce au ON DELETE CASCADE
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM PLAYLIST
                    WHERE id_playlist = %s;
                    """,
                    (id_playlist,),
                )
            connection.commit()
