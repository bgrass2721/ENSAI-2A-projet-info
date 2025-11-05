from business_object.paroles import Paroles
from dao.dao import DAO
from dao.db_connection import DBConnection


class DAO_paroles(DAO):
    def get_paroles(self) -> list[Paroles] | None:
        """
        Liste l'objet Paroles de toutes les chansons enregistrées dans la BD
        """
        list_Paroles = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT embed_paroles, str_paroles 
                    FROM CHANSON;
                    """)  # [(embed_paroles, str_paroles), (embed_paroles, str_paroles),]
                res = cursor.fetchall()
                if res:
                    for content, vecteur in res:
                        paroles = Paroles(content=content, vecteur=vecteur)
                        list_Paroles.append(paroles)
                    return list_Paroles
