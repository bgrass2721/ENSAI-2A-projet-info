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
        Supprime une chanson de la table CHANSON, soit via le titre ET l'artiste
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
