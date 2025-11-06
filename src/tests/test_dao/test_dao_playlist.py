# Fichier: test_dao_playlist.py

import pytest
from dao.dao_playlist import DAO_playlist
from dao.dao_chanson import DAO_chanson

class TestDAOPlaylist:

    # Fixture pour s'assurer que les chansons existent en BD avant de créer une playlist
    @pytest.fixture
    def setup_chansons(self, clean_db, chanson_imagine, chanson_yesterday):
        dao_chanson = DAO_chanson()
        dao_chanson.add_chanson(chanson_imagine)
        dao_chanson.add_chanson(chanson_yesterday)
        # Retourne les objets au cas où
        return chanson_imagine, chanson_yesterday

    # 1. Tester l'ajout d'une playlist (et de ses entrées dans CATALOGUE)
    def test_01_add_playlist_success(self, clean_db, setup_chansons, playlist_avec_chansons):
        # GIVEN
        dao = DAO_playlist()

        # WHEN
        result = dao.add_playlist(playlist_avec_chansons)

        # THEN
        assert result is True
        
    # 2. Tester la récupération de toutes les playlists
    def test_02_get_plalists_success(self, clean_db, setup_chansons, playlist_avec_chansons):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_avec_chansons)

        # WHEN
        playlists = dao.get_playlists()

        # THEN
        assert playlists is not None
        assert len(playlists) == 1
        
        playlist_recuperee = playlists[0]
        assert playlist_recuperee.nom == playlist_avec_chansons.nom
        assert len(playlist_recuperee.chansons) == 2
        
        # Vérification que la récupération a bien mappé les BOs
        assert playlist_recuperee.chansons[0] == playlist_avec_chansons.chansons[0] 

    # 3. Tester la récupération par nom (requiert la correction SQL)
    def test_03_get_playlist_from_nom_success(self, clean_db, setup_chansons, playlist_avec_chansons):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_avec_chansons)

        # WHEN
        playlist = dao.get_playlist_from_nom(playlist_avec_chansons.nom)

        # THEN
        assert playlist is not None
        assert playlist.nom == playlist_avec_chansons.nom
        assert len(playlist.chansons) == 2

    # 4. Tester l'ajout d'un doublon (nom unique)
    def test_04_add_playlist_duplicate_by_nom(self, clean_db, setup_chansons, playlist_avec_chansons):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_avec_chansons)

        # WHEN
        # On essaie d'ajouter une playlist avec le même nom
        result = dao.add_playlist(playlist_avec_chansons)

        # THEN
        assert result is False # ON CONFLICT DO NOTHING -> retourne False
        assert len(dao.get_playlists()) == 1

    # 5. Tester la suppression d'une playlist
    def test_05_del_playlist_via_nom_success(self, clean_db, setup_chansons, playlist_avec_chansons):
        # GIVEN
        dao = DAO_playlist()
        dao.add_playlist(playlist_avec_chansons)
        assert len(dao.get_playlists()) == 1

        # WHEN
        result = dao._del_playlist_via_nom(playlist_avec_chansons.nom)

        # THEN
        assert result is True
        assert dao.get_playlists() is None