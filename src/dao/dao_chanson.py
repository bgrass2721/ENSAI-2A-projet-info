from business_object.chanson import Chanson
from business_object.paroles import Paroles
from dao.dao import DAO
from dao.db_connection import DBConnection


class DAO_chanson(DAO):
    def add_chanson(self, chanson: Chanson) -> None:
        """
        Ajoute une chanson à la table CHANSON de la BD
        """
        embed_paroles = chanson.paroles.vecteur
        titre = chanson.titre
        artiste = chanson.artiste
        annee = chanson.annee
        str_paroles = chanson.paroles.content
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO CHANSON (embed_paroles, titre, artiste, annee, str_paroles)
                    VALUES (%(embed_paroles)s, %(titre)s, %(artiste)s, %(annee)s, %(str_paroles)s)
                    ON CONFLICT DO NOTHING;
                    """,
                    # ON CONFLICT évite d'enregistrer deux fois une chanson
                    {
                        "embed_paroles": embed_paroles,
                        "titre": titre,
                        "artiste": artiste,
                        "annee": annee,
                        "str_paroles": str_paroles,
                    },
                )
                connection.commit()

    def get_chansons(self) -> list[Chanson]:
        """
        Liste l'objet Chanson de toutes les chansons enregistrées dans la BD
        """
        list_Chansons = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT embed_paroles, titre, artiste, annee, str_paroles FROM CHANSON;"
                )
                res = cursor.fetchall()  # liste de tuple
                for tup in res:
                    vecteur, titre, artiste, annee, content = tup
                    paroles = Paroles(content=content, vecteur=vecteur)
                    chanson = Chanson(titre, artiste, annee, paroles)
                    list_Chansons.append(chanson)
        return list_Chansons

    def get_chanson_from_embed_paroles(self, embed_paroles: list[float]) -> Chanson | None:
        # id = embed_paroles
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT titre, artiste, annee, str_paroles
                    FROM CHANSON
                    WHERE embed_paroles = %s;
                    """,
                    (embed_paroles,),
                )
                res = cursor.fetchone()  # (tire, artiste, annee)
                if res:
                    titre, artiste, annee, str_paroles = res
                    paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
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
