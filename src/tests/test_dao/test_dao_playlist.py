# Fichier: test_dao_playlist.py

import pytest
import numpy as np
from datetime import date
from business_object.paroles import Paroles
from business_object.chanson import Chanson
from business_object.playlist import Playlist
from dao.dao import DAO
from dao.dao_chanson import DAO_chanson
from dao.dao_playlist import DAO_playlist
from dao.db_connection import DBConnection
from psycopg2 import sql

# --- FIXTURES LOCALES : SETUP/TEARDOWN ---

@pytest.fixture(scope="session")
def setup_db():
    """Crée l'instance DAO une fois par session pour assurer la création des tables."""
    return DAO() 

@pytest.fixture
def clean_db(setup_db):
    """Vide toutes les tables (CATALOGUE, PLAYLIST, CHANSON) avant et après chaque test."""
    # L'ordre de suppression dans DAO._del_data_table est important (CATALOGUE, PLAYLIST, CHANSON)
    setup_db._del_data_table(None)
    yield
    setup_db._del_data_table(None)

# --- FIXTURES LOCALES : OBJETS MÉTIER PRÉ-ENREGISTRÉS ---

@pytest.fixture
def paroles_imagine():
    """Paroles de test avec un vecteur unique."""
    # Utilisation d'une petite taille et de nombres fixes pour la reproductibilité
    vecteur = [0.111, 0.222, 0.333, 0.444, 0.555, 0.666, 0.777, 0.888, 0.999, 0.123]
    return Paroles(content="Imagine there's no heaven...", vecteur=vecteur)

@pytest.fixture
def paroles_yesterday():
    """Autre paroles avec un vecteur unique."""
    vecteur = [0.999, 0.888, 0.777, 0.666, 0.555, 0.444, 0.333, 0.222, 0.111, 0.321]
    return Paroles(content="Yesterday, all my troubles seemed so far away...", vecteur=vecteur)

@pytest.fixture
def chanson_imagine(paroles_imagine):
    """Chanson complète pour les tests."""
    return Chanson("Imagine", "John Lennon", 1971, paroles_imagine)

@pytest.fixture
def chanson_yesterday(paroles_yesterday):
    """Deuxième chanson pour les tests."""
    return Chanson("Yesterday", "The Beatles", 1965, paroles_yesterday)

@pytest.fixture
def playlist_classiques(chanson_imagine, chanson_yesterday):
    """Playlist contenant deux chansons."""
    # NOTE: L'id de la Playlist n'est pas utilisé à l'instanciation, il est attribué par la BDD
    return Playlist(nom="Classiques", chansons=[chanson_imagine, chanson_yesterday])

@pytest.fixture
def add_chansons_to_db(clean_db, chanson_imagine, chanson_yesterday):
    """Ajoute les chansons nécessaires à la BDD avant les tests de playlist."""
    dao_chanson = DAO_chanson()
    # On doit s'assurer que les chansons sont bien dans CHANSON
    dao_chanson.add_chanson(chanson_imagine)
    dao_chanson.add_chanson(chanson_yesterday)
    
    # Vérification optionnelle que l'ajout a réussi
    assert dao_chanson.get_chanson(chanson_imagine.titre, chanson_imagine.artiste) is not None
    assert dao_chanson.get_chanson(chanson_yesterday.titre, chanson_yesterday.artiste) is not None

# --- FONCTION UTILITAIRE : VÉRIFIER L'ÉTAT DE LA BDD ---

def get_catalogue_count(playlist_id: int):
    """Compte le nombre d'entrées pour une playlist dans la table CATALOGUE."""
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM CATALOGUE WHERE id_playlist = %s;"),
                (playlist_id,),
            )
            return cursor.fetchone()[0]


# --- CLASSE DE TEST : DAO_playlist ---

class TestDAOPlaylist:

    # 1. Tester l'ajout d'une nouvelle playlist
    def test_01_add_playlist_success(self, add_chansons_to_db, playlist_classiques):
        # GIVEN
        dao = DAO_playlist()
        playlist = playlist_classiques
        
        # WHEN
        success = dao.add_playlist(playlist)
        
        # THEN
        assert success is True
        
        # Vérification dans la BDD
        retrieved_playlist = dao.get_playlist_from_nom(playlist.nom)
        assert retrieved_playlist is not None
        assert retrieved_playlist.nom == playlist.nom
        assert len(retrieved_playlist.chansons) == len(playlist.chansons)
        
        # Vérification du CATALOGUE (doit contenir 2 entrées)
        catalogue_count = get_catalogue_count(retrieved_playlist.id)
        assert catalogue_count == 2
        
    # 2. Tester la récupération d'une playlist par son nom
    def test_02_get_playlist_from_nom_exists(self, add_chansons_to_db, playlist_classiques):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_classiques)
        
        # WHEN
        retrieved_playlist = dao.get_playlist_from_nom(playlist_classiques.nom)
        
        # THEN
        assert retrieved_playlist is not None
        assert retrieved_playlist.nom == playlist_classiques.nom
        assert len(retrieved_playlist.chansons) == 2
        
        # Vérification des objets Chanson
        chanson_titles = {c.titre for c in retrieved_playlist.chansons}
        assert "Imagine" in chanson_titles
        assert "Yesterday" in chanson_titles

    # 3. Tester la récupération d'une playlist non existante
    def test_03_get_playlist_from_nom_not_exists(self, clean_db):
        # GIVEN
        dao = DAO_playlist()
        
        # WHEN
        result = dao.get_playlist_from_nom("Inexistante")
        
        # THEN
        assert result is None
        
    # 4. Tester l'ajout d'une playlist avec 0 chansons
    def test_04_add_playlist_empty_songs(self, clean_db):
        # GIVEN
        dao = DAO_playlist()
        playlist_vide = Playlist(nom="Vide", chansons=[])
        
        # WHEN
        success = dao.add_playlist(playlist_vide)
        
        # THEN
        # La playlist devrait être ajoutée même si elle est vide (PLAYLIST table uniquement)
        assert success is True
        retrieved_playlist = dao.get_playlist_from_nom(playlist_vide.nom)
        assert retrieved_playlist is not None
        assert len(retrieved_playlist.chansons) == 0
        
        # Vérification du CATALOGUE (doit contenir 0 entrée)
        catalogue_count = get_catalogue_count(retrieved_playlist.id)
        assert catalogue_count == 0

    # 5. Tester la récupération de toutes les playlists
    def test_05_get_playlists_multiple(self, add_chansons_to_db, playlist_classiques, chanson_imagine):
        # GIVEN
        dao = DAO_playlist()
        
        # Créer une deuxième playlist avec une seule chanson
        playlist_solo = Playlist(nom="SoloHits", chansons=[chanson_imagine])
        
        dao.add_playlist(playlist_classiques)
        dao.add_playlist(playlist_solo)
        
        # WHEN
        playlists = dao.get_playlists()
        
        # THEN
        assert playlists is not None
        assert len(playlists) == 2
        names = {p.nom for p in playlists}
        assert "Classiques" in names
        assert "SoloHits" in names
        
        # Vérification du contenu (optionnel mais bon de s'assurer du mappage)
        for p in playlists:
            if p.nom == "Classiques":
                assert len(p.chansons) == 2
            elif p.nom == "SoloHits":
                assert len(p.chansons) == 1

    # 6. Tester la suppression d'une playlist par son nom
    def test_06_del_playlist_via_nom_success(self, add_chansons_to_db, playlist_classiques):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_classiques)
        playlist_avant_suppression = dao.get_playlist_from_nom(playlist_classiques.nom)
        assert playlist_avant_suppression is not None
        
        # WHEN
        success = dao._del_playlist_via_nom(playlist_classiques.nom)
        
        # THEN
        assert success is True
        assert dao.get_playlist_from_nom(playlist_classiques.nom) is None
        
        # Vérification que les entrées CATALOGUE ont été supprimées (ON DELETE CASCADE)
        # On suppose que l'ID a été récupéré par le `get_playlist_from_nom` précédent
        catalogue_count_apres = get_catalogue_count(playlist_avant_suppression.id)
        assert catalogue_count_apres == 0

    # 7. Tester l'ajout d'une playlist avec le même nom (doit échouer - UNIQUE constraint)
    def test_07_add_playlist_duplicate_name(self, add_chansons_to_db, playlist_classiques):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_classiques)
        
        # WHEN
        # Tentative d'ajouter la même playlist
        success = dao.add_playlist(playlist_classiques)
        
        # THEN
        # ON CONFLICT DO NOTHING dans add_playlist. Si la playlist existe déjà, rowcount = 0.
        assert success is False
        
        # On vérifie qu'il n'y a qu'une seule playlist dans la BDD avec ce nom (nécessite une petite requête personnalisée)
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM PLAYLIST WHERE nom = %s;", (playlist_classiques.nom,))
                count = cursor.fetchone()[0]
                assert count == 1