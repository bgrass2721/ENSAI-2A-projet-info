import pytest
from unittest.mock import Mock, patch
from client.playlist_client import PlaylistClient
from business_object.playlist import Playlist
from business_object.chanson import Chanson

# Fixtures d'objets simulés (réutilisées)
@pytest.fixture
def mock_playlist_remplie():
    """Crée un objet Playlist simulé qui retourne des chansons."""
    mock_songs = [Mock(spec=Chanson), Mock(spec=Chanson)]
    playlist = Mock(spec=Playlist, nom="Favorites")
    playlist.get_chansons.return_value = mock_songs 
    playlist.chansons = mock_songs
    return playlist

@pytest.fixture
def mock_playlist_vide():
    """Crée un objet Playlist simulé qui retourne une liste de chansons vide."""
    playlist = Mock(spec=Playlist, nom="Empty")
    playlist.get_chansons.return_value = []
    playlist.chansons = []
    return playlist

class TestPlaylistClient:
    
    # --- Tests pour request_playlist ---
    
    @patch('client.playlist_client.DAO_playlist')
    @patch('client.playlist_client.PlaylistService')
    def test_01_request_playlist_success(self, MockService, MockDAO, mock_playlist_remplie):
        # Teste l'orchestration normale
        client = PlaylistClient()
        keyword = "rock"
        nbsongs = 10
        MockService.return_value.instantiate_playlist.return_value = mock_playlist_remplie
        
        result = client.request_playlist(keyword, nbsongs)
        
        MockService.return_value.instantiate_playlist.assert_called_once_with(keyword, nbsongs)
        MockDAO.return_value.add_playlist.assert_called_once_with(mock_playlist_remplie)
        assert result == mock_playlist_remplie
        
    # --- Tests pour get_playlists ---
    
    @patch('client.playlist_client.DAO_playlist')
    def test_02_get_playlists_returns_multiple(self, MockDAO, mock_playlist_remplie):
        # Teste le cas normal : plusieurs playlists
        client = PlaylistClient()
        expected_list = [mock_playlist_remplie, Mock(spec=Playlist)]
        MockDAO.return_value.get_playlists.return_value = expected_list
        
        result = client.get_playlists()
        
        assert result == expected_list
        
    @patch('client.playlist_client.DAO_playlist')
    def test_03_get_playlists_returns_none(self, MockDAO):
        # Teste le cas limite : base vide
        client = PlaylistClient()
        MockDAO.return_value.get_playlists.return_value = None
        
        result = client.get_playlists()
        
        assert result is None

    # --- Tests pour get_playlist (par nom) ---
    
    @patch('client.playlist_client.DAO_playlist')
    def test_04_get_playlist_by_nom_found(self, MockDAO, mock_playlist_remplie):
        # Teste la récupération réussie
        client = PlaylistClient()
        MockDAO.return_value.get_playlist_from_nom.return_value = mock_playlist_remplie
        
        result = client.get_playlist("Favorites")
        
        assert result == mock_playlist_remplie
        
    @patch('client.playlist_client.DAO_playlist')
    def test_05_get_playlist_by_nom_not_found(self, MockDAO):
        # Teste le cas non trouvé
        client = PlaylistClient()
        MockDAO.return_value.get_playlist_from_nom.return_value = None
        
        result = client.get_playlist("Inconnu")
        
        assert result is None
        
    # --- Tests pour get_playlist_chansons ---
    
    @patch('client.playlist_client.DAO_playlist')
    def test_06_get_playlist_chansons_found_and_not_empty(self, MockDAO, mock_playlist_remplie):
        # Teste la récupération réussie de la liste
        client = PlaylistClient()
        MockDAO.return_value.get_playlist_from_nom.return_value = mock_playlist_remplie
        
        result = client.get_playlist_chansons("Favorites")
        
        # S'assure que la méthode get_chansons() de la playlist mockée a été appelée
        mock_playlist_remplie.get_chansons.assert_called_once()
        assert result == mock_playlist_remplie.get_chansons.return_value 
        assert len(result) > 0

    @patch('client.playlist_client.DAO_playlist')
    def test_07_get_playlist_chansons_found_but_empty(self, MockDAO, mock_playlist_vide):
        # Teste une playlist existante mais sans chansons
        client = PlaylistClient()
        MockDAO.return_value.get_playlist_from_nom.return_value = mock_playlist_vide
        
        result = client.get_playlist_chansons("Empty")
        
        mock_playlist_vide.get_chansons.assert_called_once()
        assert result == [] # Doit retourner la liste vide

    @patch('client.playlist_client.DAO_playlist')
    def test_08_get_playlist_chansons_playlist_not_found(self, MockDAO):
        # Teste le cas où la playlist n'existe pas
        client = PlaylistClient()
        MockDAO.return_value.get_playlist_from_nom.return_value = None
        
        result = client.get_playlist_chansons("Inconnu")
        
        assert result is None