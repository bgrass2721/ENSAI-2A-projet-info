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
from business_object.paroles import Paroles
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
                connection.commit()

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
                id_playlist = cursor.fetchone()[0]
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
        Récupère l'object Paroles de toutes les chansons enregistrées dans la BD
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
