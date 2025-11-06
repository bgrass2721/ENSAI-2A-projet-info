import numpy as np
import pytest

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from dao.dao import DAO
from dao.dao_chanson import DAO_chanson

# --- FIXTURES LOCALES : SETUP/TEARDOWN ---


@pytest.fixture(scope="session")
def setup_db():
    """Crée l'instance DAO une fois par session pour assurer la création des tables."""
    return DAO()


@pytest.fixture
def clean_db(setup_db):
    """Vide toutes les tables avant et après chaque test."""
    setup_db._del_data_table(None)
    yield
    setup_db._del_data_table(None)


# --- FIXTURES LOCALES : OBJETS MÉTIER ---


@pytest.fixture
def paroles_imagine():
    """Paroles de test pour John Lennon."""
    vecteur = [round(float(x), 6) for x in np.random.rand(10)]
    return Paroles(content="Imagine there's no heaven...", vecteur=vecteur)


@pytest.fixture
def paroles_yesterday():
    """Paroles de test pour The Beatles."""
    vecteur = [round(float(x) * 0.5, 6) for x in np.random.rand(10)]
    return Paroles(content="Yesterday, all my troubles seemed so far away...", vecteur=vecteur)


@pytest.fixture
def chanson_imagine(paroles_imagine):
    """Chanson complète avec année."""
    return Chanson("Imagine", "John Lennon", 1971, paroles_imagine)


@pytest.fixture
def chanson_yesterday(paroles_yesterday):
    """Deuxième chanson complète pour les listes."""
    return Chanson("Yesterday", "The Beatles", 1965, paroles_yesterday)


@pytest.fixture
def chanson_annee_none():
    """Chanson sans année de sortie."""
    vecteur = [round(float(x) * 1.5, 6) for x in np.random.rand(10)]
    paroles = Paroles(content="Ceci est un test sans année", vecteur=vecteur)
    return Chanson("Titre Sans Annee", "Artiste Inconnu", None, paroles)


# --- CLASSE DE TEST : DAO_chanson ---


class TestDAOChanson:
    # 1. Tester l'ajout et le retour booléen
    def test_01_add_chanson_success(self, clean_db, chanson_imagine):
        dao = DAO_chanson()
        result = dao.add_chanson(chanson_imagine)
        assert result is True

    # 2. Tester l'ajout d'un doublon (ON CONFLICT DO NOTHING)
    def test_02_add_chanson_duplicate_by_embed_paroles(self, clean_db, chanson_imagine):
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)

        # On essaie d'ajouter la même chanson (même vecteur UNIQUE)
        result = dao.add_chanson(chanson_imagine)

        assert result is False
        assert len(dao.get_chansons()) == 1

    # 3. Tester la récupération de toutes les chansons
    def test_03_get_chansons_multiple_songs(self, clean_db, chanson_imagine, chanson_yesterday):
        # Ajout de plusieurs chansons
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)
        dao.add_chanson(chanson_yesterday)

        chansons = dao.get_chansons()

        assert chansons is not None
        assert len(chansons) == 2
        # On vérifie que les deux objets sont présents
        assert chanson_imagine in chansons
        assert chanson_yesterday in chansons

    # 4. Tester la récupération de toutes les chansons quand la base est vide
    def test_04_get_chansons_empty_db(self, clean_db):
        dao = DAO_chanson()
        chansons = dao.get_chansons()
        assert chansons is None  # Vérifie que None est retourné

    # 5. Tester la récupération par titre et artiste
    def test_05_get_chanson_from_titre_artiste_found(self, clean_db, chanson_imagine):
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)
        chanson = dao.get_chanson_from_titre_artiste("Imagine", "John Lennon")
        assert chanson == chanson_imagine

    # 6. Tester la récupération par titre et artiste non trouvé
    def test_06_get_chanson_from_titre_artiste_not_found(self, clean_db, chanson_imagine):
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)
        chanson = dao.get_chanson_from_titre_artiste("Imagine", "Artiste Inconnu")
        assert chanson is None

    # 7. Tester la récupération par embedding de paroles
    def test_07_get_chanson_from_embed_paroles_found(self, clean_db, chanson_imagine):
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)
        chanson = dao.get_chanson_from_embed_paroles(chanson_imagine.paroles.vecteur)
        assert chanson == chanson_imagine

    # 8. Tester la récupération par embedding de paroles non trouvé
    def test_08_get_chanson_from_embed_paroles_not_found(self, clean_db, paroles_yesterday):
        dao = DAO_chanson()
        # Aucune chanson n'est ajoutée
        chanson = dao.get_chanson_from_embed_paroles(paroles_yesterday.vecteur)
        assert chanson is None

    # 9. Tester la suppression
    def test_09_del_chanson_via_titre_artiste_success(self, clean_db, chanson_imagine):
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)

        result = dao._del_chanson_via_titre_artiste("Imagine", "John Lennon")

        assert result is True
        assert dao.get_chansons() is None

    # 10. Tester l'insertion et récupération de la donnée 'annee' (peut être NULL)
    def test_10_add_and_get_chanson_with_null_annee(self, clean_db, chanson_annee_none):
        dao = DAO_chanson()
        dao.add_chanson(chanson_annee_none)

        chanson = dao.get_chanson_from_titre_artiste(
            chanson_annee_none.titre, chanson_annee_none.artiste
        )

        assert chanson is not None
        assert chanson.annee is None
        assert chanson == chanson_annee_none
