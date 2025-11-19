import pytest
from unittest.mock import MagicMock, patch, call

from dao.dao_playlist import DAO_playlist
from business_object.playlist import Playlist
from business_object.chanson import Chanson
from business_object.paroles import Paroles

# PATCH 1: Cible la classe mère (DAO) en interdisant la connexion réelle à l'initialisation
@patch("dao.dao.DBConnection") 
# PATCH 2: Cible la classe fille (DAO_playlist) pour intercepter les appels directs aux méthodes
@patch("dao.dao_playlist.DBConnection") 
class TestDAOPlaylist:

    def setup_mocks(self, mock_dao_playlist_db, mock_dao_db):
        """Configure les mocks de connexion et de curseur."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Simuler les contextes 'with' :
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_dao_playlist_db.return_value.connection.return_value.__enter__.return_value = mock_conn
        
        return mock_cursor, mock_conn
    
    # --- FIXTURES D'OBJETS MÉTIER SIMULÉS (pour le GIVEN) ---
    @pytest.fixture
    def chanson_a_mock(self):
        # Utilisation des BOs réels pour garantir le passage de 'isinstance'
        paroles = Paroles(content="Imagine", vecteur=[0.1] * 10)
        return Chanson("Imagine", "Lennon", 1971, paroles)

    @pytest.fixture
    def chanson_b_mock(self):
        paroles = Paroles(content="Yesterday", vecteur=[0.2] * 10)
        return Chanson("Yesterday", "Beatles", 1965, paroles)

    @pytest.fixture
    def playlist_complete(self, chanson_a_mock, chanson_b_mock):
        # Utilise la signature correcte de votre BO
        return Playlist("Best Hits", [chanson_a_mock, chanson_b_mock])


    # ----------------------------------------------------------------------
    # 1. TEST : AJOUT AVEC SUCCÈS (Doit atteindre execute)
    # ----------------------------------------------------------------------
    @patch('dao.dao_playlist.DAO_playlist.__init__', return_value=None)
    def test_01_add_playlist_success(self, mock_init, mock_dao_playlist_db, mock_dao_db, playlist_complete):
        # GIVEN
        dao = DAO_playlist()
        mock_cursor, mock_conn = self.setup_mocks(mock_dao_playlist_db, mock_dao_db)
        
        # Simulation du flux de retour des ID
        mock_cursor.fetchone.side_effect = [
            {'id_playlist': 10}, # 1. Succès INSERT PLAYLIST (RETURNING)
            {'id_chanson': 1},   # 2. ID de chanson A (SELECT)
            {'id_chanson': 2},   # 3. ID de chanson B (SELECT)
        ]
        mock_cursor.rowcount = 1 # Pour les insertions CATALOGUE

        # WHEN
        res = dao.add_playlist(playlist_complete)

        # THEN
        assert res is True
        mock_conn.commit.assert_called_once()
        # On vérifie que TOUTES les requêtes ont été lancées (INSERT PLAYLIST + 2x SELECT CHANSON + 2x INSERT CATALOGUE)
        # Note: L'assertion est ajustée à 5 car le DAO exécute la requête dans la boucle.
        assert mock_cursor.execute.call_count == 5 


    # ----------------------------------------------------------------------
    # 2. TEST : CONFLIT / ÉCHEC D'AJOUT (La requête doit être appelée une seule fois)
    # ----------------------------------------------------------------------
    @patch('dao.dao_playlist.DAO_playlist.__init__', return_value=None)
    def test_02_add_playlist_conflict(self, mock_init, mock_dao_playlist_db, mock_dao_db, playlist_complete):
        # GIVEN
        dao = DAO_playlist()
        mock_cursor, mock_conn = self.setup_mocks(mock_dao_playlist_db, mock_dao_db)

        # Simuler l'échec de l'insertion PLAYLIST (fetchone est None si conflit)
        mock_cursor.fetchone.return_value = None 
        mock_cursor.rowcount = 0 

        # WHEN
        res = dao.add_playlist(playlist_complete)

        # THEN
        assert res is False
        # VÉRIFICATION : Seule la requête INSERT INTO PLAYLIST est tentée, puis le code s'arrête.
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()


    # ----------------------------------------------------------------------
    # 3. TEST : RÉCUPÉRATION PAR NOM (Succès du Mapping)
    # ----------------------------------------------------------------------
    @patch('dao.dao_playlist.DAO_playlist.__init__', return_value=None)
    def test_03_get_playlist_from_nom_success(self, mock_init, mock_dao_playlist_db, mock_dao_db, playlist_complete):
        # GIVEN
        dao = DAO_playlist()
        mock_cursor, mock_conn = self.setup_mocks(mock_dao_playlist_db, mock_dao_db)
        
        # Simuler le résultat de la jointure (RealDictCursor)
        fake_result = [
            { 'titre': 'Imagine', 'artiste': 'Lennon', 'annee': 1971, 'embed_paroles': [0.1]*10, 'str_paroles': 'Peace'},
            { 'titre': 'Yesterday', 'artiste': 'Beatles', 'annee': 1965, 'embed_paroles': [0.2]*10, 'str_paroles': 'Long ago'},
        ]
        mock_cursor.fetchall.return_value = fake_result

        # WHEN
        playlist_recup = dao.get_playlist_from_nom("Best Hits")

        # THEN
        assert playlist_recup is not None
        assert playlist_recup.nom == "Best Hits"
        # Le test doit valider que la boucle de mapping a bien tourné
        assert len(playlist_recup.chansons) == 2 
        
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_not_called()