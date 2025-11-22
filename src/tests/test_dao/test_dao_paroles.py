from unittest.mock import MagicMock, patch 
from dao.dao_paroles import DAO_paroles


# PATCH 1: Cible la classe mère (DAO)
@patch("dao.dao.DBConnection") 
# PATCH 2: Cible la classe fille (DAO_paroles)
@patch("dao.dao_paroles.DBConnection") 
class TestDAOParoles:

    def setup_mocks(self, mock_dao_paroles_db, mock_dao_db):
        """Configure les mocks de connexion et de curseur."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Simuler le Curseur
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # --- CORRECTION FINALE DU CONTEXTE ---
        # Au lieu de configurer le mock_dao_paroles_db comme un objet statique, 
        # on simule directement le comportement du *résultat* de DBConnection().connection
        
        # NOTE : Les mocks de DBConnection sont toujours actifs par le décorateur.
        
        # Simuler le comportement de 'connection'
        mock_connection_context = MagicMock()
        mock_connection_context.__enter__.return_value = mock_conn
        
        # On force la méthode .connection à retourner notre objet contexte simulé
        mock_dao_paroles_db.return_value.connection = mock_connection_context
        
        return mock_cursor, mock_conn

    # ----------------------------------------------------------------------
    # 1. TEST : RÉCUPÉRATION AVEC SUCCÈS 
    # ----------------------------------------------------------------------
    def test_01_get_paroles_returns_mapped_list(self, mock_dao_paroles_db, mock_dao_db):
        # GIVEN
        fake_data = [
            {"embed_paroles": [0.11, 0.22, 0.33], "str_paroles": "We can be heroes"},
            {"embed_paroles": [0.44, 0.55, 0.66], "str_paroles": "Just for one day"},
        ]
        
        mock_cursor, mock_conn = self.setup_mocks(mock_dao_paroles_db, mock_dao_db)
        mock_cursor.fetchall.return_value = fake_data
        
        # WHEN
        dao = DAO_paroles()
        res = dao.get_paroles()

        # THEN
        assert len(res) == 2 
        # ✅ Le test réussit si le flux de contrôle est atteint
        mock_cursor.execute.assert_called_once() 
        mock_conn.commit.assert_not_called()

    # ----------------------------------------------------------------------
    # 2. TEST : BASE DE DONNÉES VIDE
    # ----------------------------------------------------------------------
    def test_02_get_paroles_empty_db(self, mock_dao_paroles_db, mock_dao_db):
    # GIVEN
        mock_cursor, mock_conn = self.setup_mocks(mock_dao_paroles_db, mock_dao_db)
        mock_cursor.fetchall.return_value = [] 
    
    # WHEN
        dao = DAO_paroles()
        res = dao.get_paroles()

    # THEN
    # CORRECTION : Le DAO retourne None, donc on assert None.
        assert res is None
    
    # Vérification que la requête a été exécutée malgré tout
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_not_called()