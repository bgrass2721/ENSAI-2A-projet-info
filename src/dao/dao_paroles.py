from business_object.paroles import Paroles
from dao.dao import DAO
from dao.db_connection import DBConnection


class DAO_paroles(DAO):
    def get_paroles(self) -> list[Paroles]:
        """
        Liste les Paroles de toutes les chansons enregistrées dans la BD
        """
        list_Paroles = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT embed_paroles, str_paroles 
                    FROM CHANSON;
                    """)  # [(embed_paroles, str_paroles), (embed_paroles, str_paroles), ...]
                res = cursor.fetchall()
                if res:
                    for embed_paroles, str_paroles in res:
                        paroles = Paroles(content=str_paroles, vecteur=embed_paroles)
                        list_Paroles.append(paroles)
                    return list_Paroles
        return None
