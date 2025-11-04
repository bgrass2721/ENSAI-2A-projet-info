import pytest
import requests
from unittest.mock import Mock, patch
from business_object.chanson import Chanson # Assurez-vous que ce chemin est correct
from service.paroles_service import ParolesService # Assurez-vous que ce chemin est correct

# --- Fichier de test (test_paroles_service.py) ---

class TestParolesService:
    
    @pytest.fixture
    def chanson_simulee(self):
        """Fixture pour simuler un objet Chanson."""
        # Note: Nous supposons que Chanson a au moins des attributs titre et artiste
        class MockChanson:
            def __init__(self, titre, artiste):
                self.titre = titre
                self.artiste = artiste
        return MockChanson("My Song Title", "My Artist Name")

    def test_add_from_api_succes(self, monkeypatch, chanson_simulee):
        """Test la récupération des paroles avec succès via l'API."""
        
        # 1. Préparer la réponse simulée de l'API LRCLIB
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "plainLyrics": "These are the lyrics of the song.",
            "syncedLyrics": "[00:01.00]These are the lyrics"
        }
        
        # 2. Remplacer requests.get par la réponse simulée (MOCK)
        # requests.get est "monkeypatché" (simulé) pour retourner mock_response
        monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)
        
        # 3. Exécuter la fonction
        paroles = ParolesService.add_from_API(chanson_simulee)
        
        # 4. Assertions
        assert paroles == "These are the lyrics of the song."
        print(f"\n✓ Succès de l'API testé: {paroles}")


    def test_add_from_api_pas_de_paroles(self, monkeypatch, chanson_simulee):
        """Test le cas où l'API trouve la chanson mais ne retourne pas de paroles."""
        
        mock_response = Mock()
        mock_response.status_code = 200
        # Réponse sans le champ 'plainLyrics' ou avec 'plainLyrics' vide
        mock_response.json.return_value = {
            "error": "No lyrics found",
            "plainLyrics": "" 
        }
        
        monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)
        
        # Le print() du service est testé en vérifiant que le retour est None
        paroles = ParolesService.add_from_API(chanson_simulee)
        
        assert paroles is None
        print("\n✓ Cas 'Paroles non trouvées' testé.")


    def test_add_from_api_erreur_http(self, monkeypatch, chanson_simulee):
        """Test le cas où l'API retourne une erreur HTTP (e.g., 404, 500)."""
        
        # Simuler une erreur HTTP (par exemple, 404 Not Found)
        def mock_request_error(*args, **kwargs):
            mock_resp = Mock()
            mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")
            return mock_resp
            
        monkeypatch.setattr("requests.get", mock_request_error)
        
        # Le print() du service est testé en vérifiant que le retour est None
        paroles = ParolesService.add_from_API(chanson_simulee)
        
        assert paroles is None
        print("\n✓ Erreur HTTP (requests.exceptions.HTTPError) gérée.")

    def test_add_from_api_erreur_connexion(self, monkeypatch, chanson_simulee):
        """Test le cas où une erreur de connexion (Timeout, DNS, etc.) se produit."""
        
        # Simuler une erreur de connexion (e.g., Timeout)
        def mock_connection_error(*args, **kwargs):
            raise requests.exceptions.ConnectionError("Simulated connection timeout")
            
        monkeypatch.setattr("requests.get", mock_connection_error)
        
        # Le print() du service est testé en vérifiant que le retour est None
        paroles = ParolesService.add_from_API(chanson_simulee)
        
        assert paroles is None
        print("\n✓ Erreur de connexion (requests.exceptions.ConnectionError) gérée.")