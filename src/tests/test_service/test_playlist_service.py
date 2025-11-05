from unittest.mock import patch

import pytest

from business_object.playlist import Playlist
from service.chanson_service import ChansonService
from service.playlist_service import PlaylistService


class TestPlaylistService:
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return PlaylistService()

    @pytest.fixture
    def chanson_a(self):
        titre = "Imagine"
        artiste = "John Lennon"
        return ChansonService().instantiate_chanson(titre, artiste)

    @pytest.fixture
    def chanson_b(self):
        titre = "Hey Jude"
        artiste = "The Beatles"
        return ChansonService().instantiate_chanson(titre, artiste)

    @pytest.fixture
    def chanson_c(self):
        titre = "Let It Be"
        artiste = "The Beatles"
        return ChansonService().instantiate_chanson(titre, artiste)

    @pytest.fixture
    def keyword(self):
        return "love"

    @pytest.fixture
    def playlist_vide(self):
        return Playlist(1, "vide")

    @pytest.fixture
    def playlist_pleine(self, chanson_a, chanson_b):
        # Créer une playlist contenant déjà chanson_a et chanson_b
        return Playlist(1, "vide", [chanson_a, chanson_b])

    ### 1. Tests de `instantiate_playlist`

    # def test_instantiate_playlist(self, service, keyword, chanson_a, chanson_b, chanson_c):
        

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

    def test_add_nouvelle_chanson_a_playlist_pleine(self, service, playlist_pleine, chanson_c):
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

    def test_del_chanson_non_existante(self, service, playlist_pleine, chanson_c):
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
        assert len(playlist_vide.chansons) == 0
        print("\n✓ Suppression sur playlist vide gérée.")
        print("\n✓ Suppression sur playlist vide gérée.")
