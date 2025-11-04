import pytest

# from business_object.playlist import Playlist  # Décommenter si les vrais BO sont disponibles
from business_object.chanson import Chanson  # Décommenter si les vrais BO sont disponibles
from service.chanson_service import ChansonService  # Assurez-vous que ce chemin est correct


# --- Définitions simplifiées des Business Objects pour les tests ---
class MockChanson:
    """Simule la classe Chanson."""

    def __init__(self, id):
        # Un ID est crucial pour l'unicité et la comparaison
        self.id = id

    # Redéfinir __eq__ et __hash__ est nécessaire pour 'in' et 'remove'
    def __eq__(self, other):
        return isinstance(other, MockChanson) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


class MockPlaylist:
    """Simule la classe Playlist."""

    def __init__(self, chansons=None):
        self.chansons = chansons if chansons is not None else []


# -----------------------------------------------------------------


class TestChansonService:
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return ChansonService()

    @pytest.fixture
    def chanson_a(self):
        return MockChanson(id=1)

    @pytest.fixture
    def chanson_b(self):
        return MockChanson(id=2)

    ### 2. Tests de `instantiate_chanson`

    def test_instantiate_chanson(self, service):
        # GIVEN
        chanson = service.instantiate_chanson("Hey Jude", "The Beatles")

        # WHEN
        paroles = chanson.paroles

        # THEN
        assert paroles is None

    def test_add_chanson_paroles(self, service):
        chanson = service.instantiate_chanson("Hey Jude", "The Beatles")
        service.add_chanson_paroles(chanson)

        assert isinstance(chanson, Chanson)
