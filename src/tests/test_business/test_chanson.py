from business_object.chanson import Chanson
from business_object.paroles import Paroles


class TestChanson:
    def test_afficher_avec_annee(self):
        # GIVEN
        chanson = Chanson("Imagine", "John Lennon", 1971)

        # WHEN
        texte = chanson.afficher()

        # THEN
        assert texte == "Imagine - John Lennon (1971)"

    def test_afficher_sans_annee(self):
        # GIVEN
        chanson = Chanson("Hey Jude", "The Beatles")

        # WHEN
        texte = chanson.afficher()

        # THEN
        assert texte == "Hey Jude - The Beatles"

    def test_chanson_peut_avoir_paroles(self):
        # GIVEN
        p = Paroles("Imagine there's no heaven...")
        chanson = Chanson("Imagine", "John Lennon", 1971, paroles=p)

        # WHEN
        resultat = chanson.paroles.afficher()

        # THEN
        assert resultat == "Imagine there's no heaven..."
        assert isinstance(chanson.paroles, Paroles)

    def test_chanson_sans_paroles(self):
        # GIVEN
        chanson = Chanson("Let It Be", "The Beatles")

        # THEN
        assert chanson.paroles is None
