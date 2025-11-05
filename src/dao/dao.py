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
                    nom VARCHAR(255) NOT NULL, 
                    date_creation DATE DEFAULT CURRENT_DATE
                    );
                    CREATE TABLE IF NOT EXISTS CHANSON (
                    embed_paroles FLOAT8[] PRIMARY KEY,
                    titre VARCHAR(255) NOT NULL,
                    artiste VARCHAR(255) NOT NULL,
                    str_paroles TEXT NOT NULL,
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

    def del_data_table(self, nom_table: str | None) -> None:
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
