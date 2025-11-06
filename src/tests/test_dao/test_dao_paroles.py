
import pytest
import numpy as np
from business_object.paroles import Paroles
from business_object.chanson import Chanson
from dao.dao_paroles import DAO_paroles
from dao.dao_chanson import DAO_chanson
from dao.dao import DAO 

# --- FIXTURES LOCALES : SETUP/TEARDOWN ---

@pytest.fixture(scope="session")
def setup_db():
    """Crée l'instance DAO une fois par session pour assurer la création des tables."""
    return DAO() 

@pytest.fixture
def clean_db(setup_db):
    """Vide toutes les tables (CATALOGUE, PLAYLIST, CHANSON) avant et après chaque test."""
    setup_db._del_data_table(None)
    yield
    setup_db._del_data_table(None)

# --- FIXTURES LOCALES : OBJETS MÉTIER ---

@pytest.fixture
def paroles_imagine():
    """Paroles de test avec un vecteur unique."""
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
    """Deuxième chanson pour les tests."""
    return Chanson("Yesterday", "The Beatles", 1965, paroles_yesterday)

# --- CLASSE DE TEST : DAO_paroles ---

class TestDAOParoles:
    
    # 1. Tester la récupération quand la table CHANSON est vide
    def test_01_get_paroles_empty_db(self, clean_db):
        # GIVEN
        dao = DAO_paroles()

        # WHEN
        result = dao.get_paroles()

        # THEN
        # Le DAO doit retourner None si fetchall() est vide
        assert result is None
    
    # 2. Tester la récupération des paroles d'une seule chanson
    def test_02_get_paroles_one_song(self, clean_db, chanson_imagine):
        # GIVEN
        dao_chanson = DAO_chanson()
        dao_paroles = DAO_paroles()
        dao_chanson.add_chanson(chanson_imagine)

        # WHEN
        paroles_list = dao_paroles.get_paroles()

        # THEN
        assert paroles_list is not None
        assert len(paroles_list) == 1
        
        # Vérifie que les données ont été mappées correctement
        paroles_recuperees = paroles_list[0]
        assert isinstance(paroles_recuperees, Paroles)
        assert paroles_recuperees.content == chanson_imagine.paroles.content
        assert paroles_recuperees.vecteur == chanson_imagine.paroles.vecteur
        
    # 3. Tester la récupération des paroles de plusieurs chansons
    def test_03_get_paroles_multiple_songs(self, clean_db, chanson_imagine, chanson_yesterday):
        # GIVEN
        dao_chanson = DAO_chanson()
        dao_paroles = DAO_paroles()
        dao_chanson.add_chanson(chanson_imagine)
        dao_chanson.add_chanson(chanson_yesterday)

        # WHEN
        paroles_list = dao_paroles.get_paroles()

        # THEN
        assert paroles_list is not None
        assert len(paroles_list) == 2
        
        # Vérification du contenu des deux chansons (utilisation des ensembles pour l'ordre)
        contents = {p.content for p in paroles_list}
        assert chanson_imagine.paroles.content in contents
        assert chanson_yesterday.paroles.content in contents
        
    # 4. Tester l'ordre de récupération des vecteurs/paroles
    def test_04_get_paroles_vecteurs_integrity(self, clean_db, chanson_imagine):
        # GIVEN
        dao_chanson = DAO_chanson()
        dao_paroles = DAO_paroles()
        dao_chanson.add_chanson(chanson_imagine)
        
        # WHEN
        paroles_list = dao_paroles.get_paroles()

        # THEN
        # Vérifie que le vecteur récupéré est identique à celui inséré
        assert np.array_equal(paroles_list[0].vecteur, chanson_imagine.paroles.vecteur)