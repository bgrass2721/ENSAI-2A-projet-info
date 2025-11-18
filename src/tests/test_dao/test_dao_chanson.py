import pytest
from unittest.mock import MagicMock, patch 

from dao.dao_chanson import DAO_chanson
from business_object.chanson import Chanson
from business_object.paroles import Paroles

# PATCH 1: Cible la classe mère (DAO)
@patch("dao.dao.DBConnection") 
# PATCH 2: Cible la classe fille (DAO_chanson)
@patch("dao.dao_chanson.DBConnection") 
class TestDAOChanson:

    def setup_mocks(self, mock_chanson_db, mock_dao_db):
        """Configure les mocks de connexion et de curseur."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Simuler les contextes 'with' :
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_chanson_db.return_value.connection.return_value.__enter__.return_value = mock_conn
        
        return mock_cursor, mock_conn

    def test_add_chanson_echec_insertion(self, mock_chanson_db, mock_dao_db):
        # GIVEN
        paroles = Paroles(content="duplicate", vecteur=[0.5, 0.6])
        chanson = Chanson("Duplicate", "Artist", 2020, paroles)
        
        mock_cursor, mock_conn = self.setup_mocks(mock_chanson_db, mock_dao_db)
        mock_cursor.rowcount = 0  # Simule un ON CONFLICT DO NOTHING (échec)

        # WHEN
        dao = DAO_chanson()
        res = dao.add_chanson(chanson)

        # THEN
        assert res is False
        # Si rowcount est 0, le commit ne doit pas être appelé (bonne pratique).
        mock_conn.commit.assert_not_called()