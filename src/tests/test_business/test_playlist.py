from business_layer.playlist import Playlist
from business_layer.chanson import Chanson


class TestPlaylist:
    def test_afficher_playlist_vide(self):
        # GIVEN
        playlist = Playlist(1, "Classiques")

        # WHEN
        texte = playlist.afficher()

        # THEN
        assert texte == "Playlist 'Classiques' (vide)"

    def test_afficher_playlist_avec_chansons(self):
        # GIVEN
        c1 = Chanson(1, "Imagine", "John Lennon", 1971)
        c2 = Chanson(2, "Hey Jude", "The Beatles", 1968)
        playlist = Playlist(1, "Classiques", [c1, c2])

        # WHEN
        texte = playlist.afficher()

        # THEN
        assert "Imagine - John Lennon (1971)" in texte
        assert "Hey Jude - The Beatles (1968)" in texte

    def test_get_chansons_retourne_liste(self):
        # GIVEN
        c1 = Chanson(1, "Imagine", "John Lennon", 1971)
        playlist = Playlist(1, "Classiques", [c1])

        # WHEN
        chansons = playlist.get_chansons()

        # THEN
        assert isinstance(chansons, list)
        assert chansons[0] == c1

    def test_playlist_peut_etre_modifiee_dynamiquement(self):
        # GIVEN
        c1 = Chanson(1, "Imagine", "John Lennon", 1971)
        c2 = Chanson(2, "Yesterday", "The Beatles", 1965)
        playlist = Playlist(1, "Années 60")

        # WHEN
        playlist.chansons.append(c1)
        playlist.chansons.append(c2)

        # THEN
        assert len(playlist.chansons) == 2
        assert playlist.chansons[1].titre == "Yesterday"
