from business_object.chanson import Chanson
from business_object.paroles import Paroles
from dao.dao import DAO
from dao.db_connection import DBConnection


class DAO_chanson(DAO):
    def add_chanson(self, chanson: Chanson) -> None:
        """
        Ajoute une chanson à la table CHANSON de la BD
        """
        if not isinstance(chanson, Chanson):
            raise TypeError("chanson not Chanson")
        if not isinstance(chanson.paroles, Paroles):
            raise TypeError("chanson.paroles not Paroles")
        if not isinstance(chanson.titre, str):
            raise ValueError("chanson.titre not str")
        if not isinstance(chanson.artiste, str):
            raise ValueError("chanson.artiste not str")
        if not (isinstance(chanson.annee, int) or chanson.annee is None):
            raise TypeError("chanson.annee not int or None")
        if not isinstance(chanson.paroles.vecteur, list):
            raise TypeError("chanson.paroles.vecteur not list")
        if not all(isinstance(x, (int, float)) for x in chanson.paroles.vecteur):
            raise TypeError("chanson.paroles.vecteur not list")
        if not isinstance(chanson.paroles.content, str):
            raise TypeError("chanson.paroles.content not str")
        """
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                modif = 0
                # si la requête n'est pas correcte, modif ne serait pas initialisée
                # correcte si : requête correcte, requête correcte avec valeur dupliquée
                cursor.execute(
                    """
                    INSERT INTO CHANSON (titre, artiste, annee, embed_paroles, str_paroles)
                    VALUES (%(titre)s, %(artiste)s, %(annee)s, %(embed_paroles)s, %(str_paroles)s)
                    ON CONFLICT DO NOTHING;
                    """,
                    # ON CONFLICT DO NOTHING pour les attributs UNIQUE
                    {
                        "titre": chanson.titre,
                        "artiste": chanson.artiste,
                        "annee": chanson.annee,
                        "embed_paroles": [round(x, 6) for x in chanson.paroles.vecteur],
                        "str_paroles": chanson.paroles.content,
                    },
                )
                modif += cursor.rowcount
                connection.commit()
        return modif == 1

    def get_chansons(self) -> list[Chanson] | None:
        """
        Liste toutes les Chanson enregistrées dans la BD
        """
        list_Chansons = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT titre, artiste, annee, embed_paroles, str_paroles
                    FROM CHANSON;
                    """)  # [(titre, artiste, annee, embed_paroles, str_paroles), (...), ...]
                res = cursor.fetchall() or None
                if res:  # None traité comme False : la condition n'est pas remplie
                    for chanson in res:
                        paroles = Paroles(
                            content=chanson["str_paroles"], vecteur=chanson["embed_paroles"]
                        )
                        chanson = Chanson(
                            titre=chanson["titre"],
                            artiste=chanson["artiste"],
                            annee=chanson["annee"],
                            paroles=paroles,
                        )
                        list_Chansons.append(chanson)
                    return list_Chansons

    def get_chanson_from_embed_paroles(self, embed_paroles: list[float]) -> Chanson | None:
        """
        Récupère un object Chanson via l'embedding de paroles
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT titre, artiste, annee, embed_paroles, str_paroles
                    FROM CHANSON
                    WHERE embed_paroles = %s::float8[];
                    """,
                    (embed_paroles,),
                )  # (tire, artiste, annee, embed_paroles, str_paroles)
                res = cursor.fetchone()
                if res:
                    paroles = Paroles(content=res["str_paroles"], vecteur=res["embed_paroles"])
                    chanson = Chanson(
                        titre=res["titre"],
                        artiste=res["artiste"],
                        annee=res["annee"],
                        paroles=paroles,
                    )
                    return chanson

    def get_chanson_from_titre_artiste(self, titre: str, artiste: str) -> Chanson | None:
        """
        Récupère une Chanson via l'embedding de paroles
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT titre, artiste, annee, embed_paroles, str_paroles
                    FROM CHANSON
                    WHERE titre = %s
                    AND artiste = %s;
                    """,
                    (titre, artiste),
                )  # (tire, artiste, annee, embed_paroles, str_paroles)
                res = cursor.fetchone()
                if res:
                    paroles = Paroles(content=res["str_paroles"], vecteur=res["embed_paroles"])
                    chanson = Chanson(
                        titre=res["titre"],
                        artiste=res["artiste"],
                        annee=res["annee"],
                        paroles=paroles,
                    )
                    return chanson

    def _del_chanson_via_titre_artiste(self, titre: str, artiste: str) -> bool:
        """
        Supprime une chanson de la table CHANSON via l'embedding pour l'identifier
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                modif = 0
                # requête correcte si : ligne trouvée et supprimée, aucune ligne trouvée
                cursor.execute(
                    """
                    DELETE FROM CHANSON
                    WHERE titre = %s
                    AND artiste = %s;
                    """,
                    (titre, artiste),
                )
                modif += cursor.rowcount
                connection.commit()
        return modif == 1
