# Fichier: test_dao_paroles.py

import pytest
from dao.dao_paroles import DAO_paroles
from dao.dao_chanson import DAO_chanson

class TestDAOParoles:
    
    # 1. Tester la récupération de toutes les paroles (base vide)
    def test_01_get_paroles_empty_db(self, clean_db):
        # GIVEN
        dao = DAO_paroles()

        # WHEN
        result = dao.get_paroles()

        # THEN
        assert result is None
    
    # 2. Tester la récupération de toutes les paroles (chansons insérées)
    def test_02_get_paroles_success(self, clean_db, chanson_imagine, chanson_yesterday):
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
        # Vérification simple du contenu
        contents = [p.content for p in paroles_list]
        assert chanson_imagine.paroles.content in contents
        assert chanson_yesterday.paroles.content in contents