import pytest
from unittest.mock import Mock, patch
from client.chanson_client import ChansonClient
from business_object.chanson import Chanson 
from business_object.paroles import Paroles 

# Fixtures d'objets simulés (réutilisées)
@pytest.fixture
def mock_chanson_avec_paroles():
    """Crée un objet Chanson simulé avec des paroles."""
    paroles = Mock(spec=Paroles, content="Contenu des paroles test", vecteur=[0.1, 0.2])
    chanson = Mock(spec=Chanson, titre="Titre Test", artiste="Artiste Test", paroles=paroles, annee=2023)
    return chanson

@pytest.fixture
def mock_chanson_sans_paroles():
    """Crée un objet Chanson simulé sans paroles."""
    chanson = Mock(spec=Chanson, titre="No Lyrics", artiste="Unknown", paroles=None)
    return chanson


class TestChansonClient:
    
    # --- Tests pour add_new_chanson ---
    
    @patch('client.chanson_client.DAO_chanson')
    @patch('client.chanson_client.ChansonService')
    def test_01_add_new_chanson_success(self, MockService, MockDAO, mock_chanson_avec_paroles):
        # S'assure que le service est appelé et que la DAO enregistre
        client = ChansonClient()
        MockService.return_value.instantiate_chanson.return_value = mock_chanson_avec_paroles
        
        client.add_new_chanson("Titre", "Artiste")
        
        MockService.return_value.add_chanson_paroles.assert_called_once()
        MockDAO.return_value.add_chanson.assert_called_once_with(mock_chanson_avec_paroles)

    @patch('client.chanson_client.DAO_chanson')
    @patch('client.chanson_client.ChansonService')
    def test_02_add_new_chanson_api_error_returns_message(self, MockService, MockDAO, mock_chanson_avec_paroles):
        # Teste le chemin d'erreur (try/except)
        client = ChansonClient()
        MockService.return_value.instantiate_chanson.return_value = mock_chanson_avec_paroles
        MockService.return_value.add_chanson_paroles.side_effect = Exception("Erreur API")
        
        result = client.add_new_chanson("Titre", "Artiste")
        
        assert result == "La chanson n'est pas trouvable sur l'API"
        MockDAO.return_value.add_chanson.assert_not_called()

    # --- Tests pour get_chansons ---
    
    @patch('client.chanson_client.DAO_chanson')
    def test_03_get_chansons_returns_multiple(self, MockDAO, mock_chanson_avec_paroles):
        # Teste le cas normal : plusieurs chansons
        client = ChansonClient()
        expected_list = [mock_chanson_avec_paroles, mock_chanson_avec_paroles]
        MockDAO.return_value.get_chansons.return_value = expected_list
        
        result = client.get_chansons()
        
        assert result == expected_list
        MockDAO.return_value.get_chansons.assert_called_once()
        
    @patch('client.chanson_client.DAO_chanson')
    def test_04_get_chansons_returns_empty_list(self, MockDAO):
        # Teste le cas limite : base vide
        client = ChansonClient()
        MockDAO.return_value.get_chansons.return_value = []
        
        result = client.get_chansons()
        
        assert result == []

    # --- Tests pour get_chanson (par titre/artiste) ---
    
    @patch('client.chanson_client.DAO_chanson')
    def test_05_get_chanson_by_titre_artiste_found(self, MockDAO, mock_chanson_avec_paroles):
        client = ChansonClient()
        MockDAO.return_value.get_chanson_from_titre_artiste.return_value = mock_chanson_avec_paroles
        
        result = client.get_chanson("Titre", "Artiste")
        
        assert result == mock_chanson_avec_paroles
        MockDAO.return_value.get_chanson_from_titre_artiste.assert_called_once_with("Titre", "Artiste")

    @patch('client.chanson_client.DAO_chanson')
    def test_06_get_chanson_by_titre_artiste_not_found(self, MockDAO):
        client = ChansonClient()
        MockDAO.return_value.get_chanson_from_titre_artiste.return_value = None
        
        result = client.get_chanson("Inconnu", "Inconnu")
        
        assert result is None

    # --- Tests pour get_lyrics_by_titre_artiste ---
    
    @patch('client.chanson_client.DAO_chanson')
    def test_07_get_lyrics_success_format(self, MockDAO, mock_chanson_avec_paroles):
        # Teste le formatage de la réponse
        client = ChansonClient()
        MockDAO.return_value.get_chanson_from_titre_artiste.return_value = mock_chanson_avec_paroles
        
        result = client.get_lyrics_by_titre_artiste("Titre", "Artiste")
        
        assert result == {
            "titre": "Titre Test",
            "artiste": "Artiste Test",
            "paroles": "Contenu des paroles test"
        }
        
    @patch('client.chanson_client.DAO_chanson')
    def test_08_get_lyrics_chanson_not_found(self, MockDAO):
        # Teste si la chanson n'est pas en base
        client = ChansonClient()
        MockDAO.return_value.get_chanson_from_titre_artiste.return_value = None
        
        result = client.get_lyrics_by_titre_artiste("Inconnu", "Inconnu")
        
        assert result is None
        
    @patch('client.chanson_client.DAO_chanson')
    def test_09_get_lyrics_chanson_found_but_no_paroles_content(self, MockDAO, mock_chanson_sans_paroles):
        # Teste si la chanson est en base mais n'a pas de contenu paroles
        client = ChansonClient()
        MockDAO.return_value.get_chanson_from_titre_artiste.return_value = mock_chanson_sans_paroles
        
        result = client.get_lyrics_by_titre_artiste("No Lyrics", "Unknown")
        
        assert result is None