# Fichier: conftest.py

import pytest
import numpy as np
from business_object.chanson import Chanson
from business_object.paroles import Paroles
from business_object.playlist import Playlist
from dao.dao import DAO

# --- Configuration de la Base de Données ---

@pytest.fixture(scope="session")
def setup_db():
    """Crée l'instance DAO une fois par session pour assurer la création des tables."""
    return DAO()

@pytest.fixture
def clean_db(setup_db):
    """Vide toutes les tables (CATALOGUE, PLAYLIST, CHANSON) avant et après chaque test."""
    # Setup : vide la DB
    setup_db._del_data_table(None)
    yield
    # Teardown : vide la DB après le test
    setup_db._del_data_table(None)

# --- Fixtures d'Objets Métier (Chansons et Paroles) ---

@pytest.fixture
def paroles_imagine():
    """Paroles pour une chanson de test."""
    # Crée un vecteur aléatoire, simulé
    vecteur = [round(float(x), 6) for x in np.random.rand(10)]
    return Paroles(content="Imagine there's no heaven...", vecteur=vecteur)

@pytest.fixture
def paroles_yesterday():
    """Autre paroles avec un vecteur unique."""
    vecteur = [round(float(x) * 0.5, 6) for x in np.random.rand(10)]
    return Paroles(content="Yesterday, all my troubles seemed so far away...", vecteur=vecteur)

@pytest.fixture
def chanson_imagine(paroles_imagine):
    """Chanson complète pour les tests."""
    return Chanson("Imagine", "John Lennon", 1971, paroles_imagine)

@pytest.fixture
def chanson_yesterday(paroles_yesterday):
    """Deuxième chanson pour les listes et playlists."""
    return Chanson("Yesterday", "The Beatles", 1965, paroles_yesterday)

# --- Fixture d'Objets Métier (Playlists) ---

@pytest.fixture
def playlist_classiques():
    """Playlist vide pour les tests d'ajout."""
    # Le constructeur corrigé (nom, chansons, id) est supposé être utilisé
    return Playlist(nom="Classiques Du Monde")

@pytest.fixture
def playlist_avec_chansons(chanson_imagine, chanson_yesterday):
    """Playlist pré-remplie pour les tests de récupération."""
    return Playlist(nom="Meilleures Ballades", chansons=[chanson_imagine, chanson_yesterday])