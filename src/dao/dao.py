"""
get_paroles() : list[Paroles]
get_playlist() : list[Playlist]
get_chanson_from_paroles() : Chanson
add_chanson(Chanson)
add_playlist(Playlist)


def add_attack(self, attack: AbstractAttack) -> bool:
        created = False

        # Get the id type
        id_attack_type = TypeAttackDAO().find_id_by_label(attack.type)
        if id_attack_type is None:
            return created

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tp.attack (id_attack_type, attack_name,        "
                    " power, accuracy, element, attack_description)             "
                    "VALUES                                                     "
                    "(%(id_attack_type)s, %(name)s, %(power)s, %(accuracy)s,    "
                    " %(element)s, %(description)s)                             "
                    "RETURNING id_attack;",
                    {
                        "id_attack_type": id_attack_type,
                        "name": attack.name,
                        "power": attack.power,
                        "accuracy": attack.accuracy,
                        "element": attack.element,
                        "description": attack.description,
                    },
                )
                res = cursor.fetchone()
        if res:
            attack.id = res["id_attack"]
            created = True

        return created

"""

from business_object.chanson import Chanson
from business_object.playlist import Playlist
from dao.db_connection import DBConnection


class DAO:
    def __init__(self):
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

    def add_chanson(self, chanson: Chanson):
        embed_paroles = chanson.paroles.vecteur
        titre = chanson.titre
        artiste = chanson.artiste
        annee = chanson.annee
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO CHANSON (embed_paroles, titre, artiste, annee)
                    VALUES (%(embed_paroles)s, %(titre)s, %(artiste)s, %(annee)s);
                    """,
                    {
                        "embed_paroles": embed_paroles,
                        "titre": titre,
                        "artiste": artiste,
                        "annee": annee,
                    },
                )

    def add_playlist(self, playlist: Playlist):
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
                id_playlist = cursor.fetchone()
                for chanson in chansons:
                    embed_paroles = chanson.paroles.vecteur
                    cursor.execute(
                        """
                        INSERT INTO CATALOGUE (id_playlist, embed_paroles)
                        VALUES (%s, %s);
                        """,
                        (id_playlist, embed_paroles),
                    )
