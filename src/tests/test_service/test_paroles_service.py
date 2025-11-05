from unittest.mock import Mock

import pytest
import requests

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from service.paroles_service import ParolesService

# --- Fichier de test (test_paroles_service.py) ---


class TestParolesService:
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return ParolesService()

    @pytest.fixture
    def chanson_correcte(self):
        titre = "Imagine"
        artiste = "John Lennon"
        return Chanson(titre, artiste)

    @pytest.fixture
    def chanson_incorrecte(self):
        titre = "blablabla"
        artiste = "jsp"
        return Chanson(titre, artiste)

    def test_add_from_api_succes(self, service, chanson_correcte):
        """Teste la récupération des paroles avec succès via l'API."""
        paroles = service.add_from_API(chanson_correcte)

        assert isinstance(paroles, Paroles)
        assert isinstance(paroles.content, str)
        print(f"\n✓ Succès de l'API testé: {paroles}")

    def test_add_from_api_pas_de_paroles(self, service, chanson_incorrecte):
        """Teste le cas où l'API ne retourne pas de paroles."""
        # Le print() du service est testé en vérifiant que le retour est None
        paroles = service.add_from_API(chanson_incorrecte)

        assert paroles is None
        print("\n✓ Cas 'Paroles non trouvées' testé.")

    def test_add_from_api_erreur_http(self, monkeypatch, service, chanson_correcte):
        """Teste le cas où l'API retourne une erreur HTTP (e.g., 404, 500)."""

        # Simuler une erreur HTTP (par exemple, 404 Not Found)
        def mock_request_error(*args, **kwargs):
            mock_resp = Mock()
            mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
                "404 Client Error: Not Found"
            )
            return mock_resp

        monkeypatch.setattr("requests.get", mock_request_error)

        # Le print() du service est testé en vérifiant que le retour est None
        paroles = service.add_from_API(chanson_correcte)

        assert paroles is None
        print("\n✓ Erreur HTTP (requests.exceptions.HTTPError) gérée.")

    def test_add_from_api_erreur_connexion(self, monkeypatch, service, chanson_correcte):
        """Test le cas où une erreur de connexion (Timeout, DNS, etc.) se produit."""

        # Simuler une erreur de connexion (e.g., Timeout)
        def mock_connection_error(*args, **kwargs):
            raise requests.exceptions.ConnectionError("Simulated connection timeout")

        monkeypatch.setattr("requests.get", mock_connection_error)

        # Le print() du service est testé en vérifiant que le retour est None
        paroles = service.add_from_API(chanson_correcte)

        assert paroles is None
        print("\n✓ Erreur de connexion (requests.exceptions.ConnectionError) gérée.")
