from abc import ABC

from dao.db_connection import DBConnection


class DAO(ABC):
    def __init__(self):
        """
        Crée la BD si elle n'est pas créée
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PLAYLIST (
                    id_playlist SERIAL PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL UNIQUE, 
                    date_creation DATE DEFAULT CURRENT_DATE
                    );
                    CREATE TABLE IF NOT EXISTS CHANSON (
                    id_chanson SERIAL PRIMARY KEY, 
                    titre VARCHAR(255) NOT NULL,
                    artiste VARCHAR(255) NOT NULL,
                    annee INT, 
                    embed_paroles FLOAT8[] NOT NULL UNIQUE,
                    str_paroles TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS CATALOGUE (
                    id_playlist SERIAL NOT NULL,
                    id_chanson SERIAL NOT NULL,
                    PRIMARY KEY (id_playlist, id_chanson),
                    FOREIGN KEY (id_playlist) REFERENCES PLAYLIST(id_playlist) ON DELETE CASCADE,
                    FOREIGN KEY (id_chanson) REFERENCES CHANSON(id_chanson) ON DELETE CASCADE
                    );
                    """)
                connection.commit()

    def del_data_table(self, nom_table: str | None) -> None:
        """
        Vide complètement les tables passées en argument.
        Si aucune table n'est spécifiée, vide toutes les tables sont vidées
        """
        # Ordre logique de suppression pour respecter les contraintes FK
        ordre = ["CATALOGUE", "PLAYLIST", "CHANSON"]
        if nom_table in ordre:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {nom_table};")
                connection.commit()
        elif nom_table is None:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    for nom_table in ordre:
                        cursor.execute(f"DELETE FROM {nom_table};")
                connection.commit()
        else:
            return None
