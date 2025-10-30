from business_object.chanson import Chanson
from business_object.paroles import Paroles
from business_object.playlist import Playlist
from dao.db_connection import DBConnection


class DAO:
    def __init__(self):
        """
        Crée la BD si elle n'est pas créée
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PLAYLIST (
                    id_playlist SERIAL PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL, 
                    date_creation DATE DEFAULT CURRENT_DATE
                    );
                    CREATE TABLE IF NOT EXISTS CHANSON (
                    embed_paroles FLOAT8[] PRIMARY KEY,
                    titre VARCHAR(255) NOT NULL,
                    artiste VARCHAR(255) NOT NULL,
                    annee INT
                    );
                    CREATE TABLE IF NOT EXISTS CATALOGUE (
                    id_playlist INT NOT NULL,
                    embed_paroles FLOAT8[] NOT NULL,
                    PRIMARY KEY (id_playlist, embed_paroles),
                    FOREIGN KEY (id_playlist) REFERENCES PLAYLIST(id_playlist) ON DELETE CASCADE,
                    FOREIGN KEY (embed_paroles) REFERENCES CHANSON(embed_paroles) ON DELETE CASCADE
                    );
                    """)
                connection.commit()

    def add_chanson(self, chanson: Chanson) -> None:
        """
        Ajoute une chanson à la table CHANSON de la BD
        """
        embed_paroles = chanson.paroles.vecteur
        titre = chanson.titre
        artiste = chanson.artiste
        annee = chanson.annee
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO CHANSON (embed_paroles, titre, artiste, annee)
                    VALUES (%(embed_paroles)s, %(titre)s, %(artiste)s, %(annee)s)
                    ON CONFLICT DO NOTHING;
                    """,
                    # ON CONFLICT évite d'enregistrer deux fois une chanson
                    {
                        "embed_paroles": embed_paroles,
                        "titre": titre,
                        "artiste": artiste,
                        "annee": annee,
                    },
                )
                connection.commit()

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

    def get_paroles(self) -> list[Paroles]:
        """
        Liste l'objet Paroles de toutes les chansons enregistrées dans la BD
        """
        list_Paroles = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT embed_paroles FROM CHANSON;")
                resultat = cursor.fetchall()  # liste de tuple
                for tup in resultat:
                    vecteur = tup[0]
                    paroles = Paroles(vecteur)
                    list_Paroles.append(paroles)
        return list_Paroles

    def get_playlists(self) -> list[Playlist]:
        """
        Liste tous les objets Playlist des playlists enregistrés dans la BD
        """
        playlists = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # récupération de l'identifiant de chaque playlist
                cursor.execute("SELECT id_playlist, nom from PLAYLIST;")
                tup_playlists = cursor.fetchall()  # [(id, nom), (id, nom), ...]
                # récupération des chansons de chaque playlist
                for id_playlist, nom in tup_playlists:
                    cursor.execute(
                        """
                        SELECT c.embed_paroles, c.titre, c.artiste, c.annee
                        FROM CHANSON c
                        JOIN CATALOGUE cat ON c.embed_paroles = cat.embed_paroles
                        WHERE cat.id_playlist = %s;
                        """,
                        (id_playlist,),
                    )
                    tup_chansons = cursor.fetchall()
                    # création liste d'objets Chanson
                    chansons = []
                    for embed_paroles, titre, artiste, annee in tup_chansons:
                        paroles = Paroles(embed_paroles)
                        chanson = Chanson(titre, artiste, annee, paroles)
                        chansons.append(chanson)
                    # création objet Playlist
                    playlist = Playlist(nom, chansons)
                    # ajout de la playlist à la liste des playlists
                    playlists.append(playlist)
            return playlists

    def get_chanson_from_paroles(self, paroles: Paroles) -> Chanson | None:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT titre, artiste, annee
                    FROM CHANSON
                    WHERE embed_paroles = %s;
                    """,
                    (paroles.vecteur,),
                )
                res = cursor.fetchone()  # (tire, artiste, annee)
                if res:
                    titre, artiste, annee = res
                    return Chanson(titre, artiste, annee, paroles)
        return None

    def del_chanson_via_embed_paroles(self, embed_paroles: list[float]) -> None:
        """
        Supprime une chanson de la table CHANSON, soit via l'embedding de ses paroles
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM CHANSON
                    WHERE embed_paroles = %s;
                    """,
                    (embed_paroles,),
                )
            connection.commit()

    def del_chanson_via_titre_artiste(self, titre: str, artiste: str) -> None:
        """
        Supprime une chanson de la table CHANSON, soit via l'embedding de ses paroles
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM CHANSON
                    WHERE titre = %s
                    AND artiste = %s;
                    """,
                    (titre, artiste),
                )
            connection.commit()

    def del_playlist_via_nom(self, nom: str) -> None:
        """
        Supprime une playlist de la table PLAYLIST via son nom.
        Les lignes associées dans CATALOGUE sont supprimées
        automatiquement grace au ON DELETE CASCADE
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM PLAYLIST
                    WHERE nom = %s;
                    """,
                    (nom,),
                )
            connection.commit()

    def del_data_table(self, nom_table: str | None = None) -> None:
        """
        Vide complètement les tables passées en argument.
        Si aucune table n'est spécifiée, vide toutes les tables sont vidées
        """
        # Ordre logique de suppression pour respecter les contraintes FK
        ordre = ["CATALOGUE", "PLAYLIST", "CHANSON"]
        if isinstance(nom_table, str) and nom_table.upper() in ordre:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {nom_table.upper()};")
            connection.commit()
        if isinstance(nom_table, None):
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    for nom_table in ordre:
                        cursor.execute(f"DELETE FROM {nom_table};")
            connection.commit()
