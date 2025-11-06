from abc import ABC

from dao.db_connection import DBConnection


class DAO(ABC):
    def __init__(self):
        """
        Crée la BD si elle n'est pas créée
        """
        self.ordre_suppr_tables = ["CATALOGUE", "PLAYLIST", "CHANSON"]
        # Ordre logique de suppression pour respecter les contraintes FK
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PLAYLIST (
                    id_playlist SERIAL PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL UNIQUE
                    );
                    CREATE TABLE IF NOT EXISTS CHANSON (
                    id_chanson SERIAL PRIMARY KEY, 
                    titre VARCHAR(255) NOT NULL,
                    artiste VARCHAR(255) NOT NULL,
                    annee INT, 
                    embed_paroles FLOAT8[] NOT NULL,
                    str_paroles TEXT NOT NULL,
                    UNIQUE(titre, artiste)
                    );
                    CREATE TABLE IF NOT EXISTS CATALOGUE (
                    id_playlist INT,
                    id_chanson INT,
                    PRIMARY KEY (id_playlist, id_chanson),
                    FOREIGN KEY (id_playlist) REFERENCES PLAYLIST(id_playlist) ON DELETE CASCADE,
                    FOREIGN KEY (id_chanson) REFERENCES CHANSON(id_chanson) ON DELETE CASCADE
                    );
                    """)
            connection.commit()

    def _del_data_table(self, nom_table: str | None) -> str | None:
        """
        Vide la table donnée en argument en majuscule
        Si aucune table n'est spécifiée, toutes les tables de la DB sont vidées
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                if nom_table in self.ordre_suppr_table:
                    cursor.execute(f"DELETE FROM {nom_table};")
                    connection.commit()
                    return "table vidée"
                if nom_table is None:
                    for nom_table in self.ordre_suppr_table:
                        cursor.execute(f"DELETE FROM {nom_table};")
                    connection.commit()
                    return "tables vidées"

    def _drop_table(self, nom_table: str | None = None) -> str | None:
        """
        Supprime la table donnée en argument en majuscule
        Si aucune table n'est spécifiée, toutes les tables de la DB sont supprimées
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                if nom_table in self.ordre_suppr_tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {nom_table} CASCADE;")
                    connection.commit()
                    return "table supprimée"
                if nom_table is None:
                    for table in self.ordre_suppr_tables:
                        cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                    connection.commit()
                    return "tables supprimées"
