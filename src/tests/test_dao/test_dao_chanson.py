
import pytest
from dao.dao_chanson import DAO_chanson

class TestDAOChanson:

    # 1. Tester l'ajout et la récupération simple
    def test_01_add_ad_get_chansons_success(self, clean_db, chanson_imagine):
        # GIVEN
        dao = DAO_chanson()

        # WHEN
        dao.add_chanson(chanson_imagine)
        chansons_recuperees = dao.get_chansons()

        # THEN
        assert chansons_recuperees is not None
        assert len(chansons_recuperees) == 1
        # Utilise la méthode __eq__ (titre et artiste)
        assert chansons_recuperees[0] == chanson_imagine
        assert chansons_recuperees[0].annee == 1971
        assert chansons_recuperees[0].paroles.content == chanson_imagine.paroles.content
        
    # 2. Tester l'ajout d'un doublon
    def test_02_add_chanson_duplicate_by_embed_paroles(self, clean_db, chanson_imagine):
        # GIVEN
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)

        # WHEN
        # On insère une chanson identique (même titre/artiste/vecteur)
        result = dao.add_chanson(chanson_imagine)

        # THEN
        assert result is None # ON CONFLICT DO NOTHING -> rowcount est 0
        assert len(dao.get_chansons()) == 1

    # 3. Tester la récupération par titre et artiste
    def test_03_get_chanson_from_titre_artiste_found(self, clean_db, chanson_imagine):
        # GIVEN
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)

        # WHEN
        chanson = dao.get_chanson_from_titre_artiste("Imagine", "John Lennon")

        # THEN
        assert chanson is not None
        assert chanson == chanson_imagine

    # 4. Tester la récupération par vecteur de paroles
    def test_04_get_chanson_from_embed_paroles_found(self, clean_db, chanson_imagine):
        # GIVEN
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)

        # WHEN
        chanson = dao.get_chanson_from_embed_paroles(chanson_imagine.paroles.vecteur)

        # THEN
        assert chanson is not None
        assert chanson == chanson_imagine

    # 5. Tester la suppression
    def test_05_del_chanson_via_titre_artiste_success(self, clean_db, chanson_imagine):
        # GIVEN
        dao = DAO_chanson()
        dao.add_chanson(chanson_imagine)
        assert len(dao.get_chansons()) == 1

        # WHEN
        result = dao._del_chanson_via_titre_artiste("Imagine", "John Lennon")

        # THEN
        assert result is True
        assert dao.get_chansons() is None

    # 6. Tester la suppression d'une chanson qui n'existe pas
    def test_06_del_chanson_not_found(self, clean_db):
        # GIVEN
        dao = DAO_chanson()

        # WHEN
        result = dao._del_chanson_via_titre_artiste("Inconnu", "Inconnu")

        # THEN
        assert result is False