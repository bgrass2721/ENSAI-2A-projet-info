import pytest

# from business_object.playlist import Playlist  # Décommenter si les vrais BO sont disponibles
# from business_object.chanson import Chanson  # Décommenter si les vrais BO sont disponibles
from service.playlist_service import PlaylistService  # Assurez-vous que ce chemin est correct


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


class TestPlaylistService:
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return PlaylistService()

    @pytest.fixture
    def chanson_a(self):
        return MockChanson(id=1)

    @pytest.fixture
    def chanson_b(self):
        return MockChanson(id=2)

    @pytest.fixture
    def playlist_vide(self):
        return MockPlaylist()

    @pytest.fixture
    def playlist_pleine(self, chanson_a, chanson_b):
        # Créer une playlist contenant déjà chanson_a et chanson_b
        return MockPlaylist(chansons=[chanson_a, chanson_b])

    ### 2. Tests de `add_chanson`

    def test_add_chanson_a_playlist_vide(self, service, playlist_vide, chanson_a):
        """Test l'ajout d'une chanson à une playlist vide."""

        # État initial: []
        assert len(playlist_vide.chansons) == 0

        service.add_chanson(playlist_vide, chanson_a)

        # État final: [chanson_a]
        assert len(playlist_vide.chansons) == 1
        assert chanson_a in playlist_vide.chansons
        print("\n✓ Ajout réussi à une playlist vide.")

    def test_add_chanson_deja_existante(self, service, playlist_pleine, chanson_a):
        """Test l'ajout d'une chanson déjà présente (ne devrait rien faire)."""

        # État initial: [chanson_a, chanson_b]
        assert len(playlist_pleine.chansons) == 2

        service.add_chanson(playlist_pleine, chanson_a)  # Ajout de chanson_a, qui est déjà là

        # La taille ne doit pas changer
        assert len(playlist_pleine.chansons) == 2
        print("\n✓ Ajout de chanson déjà existante ignoré.")

    def test_add_nouvelle_chanson_a_playlist_pleine(
        self, service, playlist_pleine, chanson_c=MockChanson(id=3)
    ):
        """Test l'ajout d'une nouvelle chanson à une playlist déjà remplie."""

        # État initial: 2 chansons
        assert len(playlist_pleine.chansons) == 2

        service.add_chanson(playlist_pleine, chanson_c)

        # État final: 3 chansons
        assert len(playlist_pleine.chansons) == 3
        assert chanson_c in playlist_pleine.chansons
        print("\n✓ Ajout réussi à une playlist pleine.")

    def test_del_chanson_existante(self, service, playlist_pleine, chanson_a):
        """Test la suppression d'une chanson existante."""

        # État initial: [chanson_a, chanson_b]
        assert len(playlist_pleine.chansons) == 2
        assert chanson_a in playlist_pleine.chansons

        service.del_chanson(playlist_pleine, chanson_a)

        # État final: [chanson_b]
        assert len(playlist_pleine.chansons) == 1
        assert chanson_a not in playlist_pleine.chansons
        print("\n✓ Suppression d'une chanson existante réussie.")

    def test_del_chanson_non_existante(self, service, playlist_pleine, chanson_c=MockChanson(id=3)):
        """Test la suppression d'une chanson qui n'est pas dans la playlist (ne devrait rien faire)."""

        # État initial: [chanson_a, chanson_b]
        assert len(playlist_pleine.chansons) == 2
        assert chanson_c not in playlist_pleine.chansons

        service.del_chanson(playlist_pleine, chanson_c)

        # La taille ne doit pas changer, et pas d'erreur ne doit être levée
        assert len(playlist_pleine.chansons) == 2
        print("\n✓ Suppression de chanson non existante ignorée.")

    def test_del_chanson_sur_playlist_vide(self, service, playlist_vide, chanson_a):
        """Test la suppression sur une playlist vide."""

        # État initial: []
        assert len(playlist_vide.chansons) == 0

        service.del_chanson(playlist_vide, chanson_a)

        # Aucune erreur, taille inchangée
        assert len(playlist_vide.chansons) == 0
        print("\n✓ Suppression sur playlist vide gérée.")
