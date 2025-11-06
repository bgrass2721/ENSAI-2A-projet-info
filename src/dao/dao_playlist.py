from itertools import groupby
from operator import itemgetter

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from business_object.playlist import Playlist
from dao.dao import DAO
from dao.db_connection import DBConnection


class DAO_playlist(DAO):
    def add_playlist(self, playlist: Playlist) -> bool:
        """
        Ajoute une playlist à la table PLAYLIST de la BD et remplit la table CATALOGUE de la BD
        """
        modif = 0
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO PLAYLIST (nom)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING
                    RETURNING id_playlist;
                    """,
                    (playlist.nom,),
                )  # (id_playlist, )
                res = cursor.fetchone()
                if res:  # si une playlist porte déjà le même nom : retourne None
                    id_playlist = res["id_playlist"]
                    chansons = playlist.chansons
                    for chanson in chansons:
                        embed_paroles = chanson.paroles.vecteur
                        # Récupération de id_chanson via l'embedding des paroles qui est unique
                        cursor.execute(
                            """
                            SELECT id_chanson 
                            FROM CHANSON
                            WHERE embed_paroles = %s::float8[];
                            """,
                            (embed_paroles,),
                        )  # (id_chanson, )
                        res = cursor.fetchone()
                        if res:
                            id_chanson = res["id_chanson"]
                            cursor.execute(
                                """
                                INSERT INTO CATALOGUE (id_playlist, id_chanson)
                                VALUES (%s, %s);
                                """,
                                (id_playlist, id_chanson),
                            )
                            modif += cursor.rowcount
                            connection.commit()
        return modif == 1

    def get_playlists(self) -> list[Playlist] | None:
        playlists = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.id_playlist,
                        p.nom, 
                        c.titre,
                        c.artiste,
                        c.annee,
                        c.embed_paroles,
                        c.str_paroles
                    FROM PLAYLIST p
                    JOIN CATALOGUE cat ON p.id_playlist = cat.id_playlist
                    JOIN CHANSON c ON cat.id_chanson = c.id_chanson
                    ORDER BY p.id_playlist;
                """)
                # ORDER BY nécessaire pour GROUP BY
                # [(id_playlist, nom, titre, artiste, annee, embed_paroles, str_paroles),
                # (...), ...]
                res = cursor.fetchall() or None
                if res:
                    # groupby et itemgetter sont natifs de Python
                    # GROUP BY id_playlist
                    # 0 car id_playlist est le premier élément de chaque tuple
                    # groupby ne marche pas avec une liste de dicos
                    list_tup = [
                        (
                            chanson["id_playlist"],
                            chanson["nom"],
                            chanson["titre"],
                            chanson["artiste"],
                            chanson["annee"],
                            chanson["embed_paroles"],
                            chanson["str_paroles"],
                        )
                        for chanson in res
                    ]
                    for id_playlist, group in groupby(list_tup, key=itemgetter(0)):
                        group = list(group)
                        # [(id_playlist, nom, titre, artiste, annee, embed_paroles, str_paroles),
                        # (...), ...] avec le même id_playlist dans chaque tuple
                        chansons = []
                        for _, _, titre, artiste, annee, embed_paroles, str_paroles in group:
                            paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
                            chanson = Chanson(titre, artiste, annee, paroles)
                            chansons.append(chanson)
                        nom = group[0][1]
                        playlist = Playlist(nom, chansons)
                        playlists.append(playlist)
                    return playlists

    def get_playlist_from_nom(self, nom: str) -> Playlist | None:
        """
        Récupère un objet Playlist à partir de son nom.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        c.titre, 
                        c.artiste, 
                        c.annee, 
                        c.embed_paroles, 
                        c.str_paroles
                    FROM PLAYLIST p
                    JOIN CATALOGUE cat ON p.id_playlist = cat.id_playlist
                    JOIN CHANSON c ON c.id_chanson = cat.id_chanson
                    WHERE p.nom = %s;
                    """,
                    (nom,),
                )
                # [(titre, artiste, annee, embed_paroles, str_paroles),
                # (...), ...]
                res = cursor.fetchall() or None
                if res:
                    chansons = []
                    for chanson in res:
                        paroles = Paroles(
                            content=chanson["str_paroles"], vecteur=chanson["embed_paroles"]
                        )
                        chanson = Chanson(
                            titre=chanson["titre"],
                            artiste=chanson["artiste"],
                            annee=chanson["annee"],
                            parole=paroles,
                        )
                        chansons.append(chanson)
                    playlist = Playlist(nom, chansons)
                    return playlist

    def _del_playlist_via_nom(self, nom: str) -> bool:
        """
        Supprime une playlist de la table PLAYLIST via son id
        Les lignes associées dans CATALOGUE sont supprimées
        automatiquement grâce au ON DELETE CASCADE
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                modif = 0
                cursor.execute(
                    """
                    DELETE FROM PLAYLIST
                    WHERE nom = %s;
                    """,
                    (nom,),
                )
                modif += cursor.rowcount
                connection.commit()
        return modif == 1
