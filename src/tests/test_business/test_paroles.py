from business_object.paroles import Paroles


class TestParoles:
    def test_afficher_retourne_contenu(self):
        # GIVEN
        texte = "Here comes the sun..."
        paroles = Paroles(content=texte)

        # WHEN
        resultat = paroles.afficher()

        # THEN
        assert resultat == texte

    def test_vecteur_est_none_par_defaut(self):
        # GIVEN / WHEN
        paroles = Paroles("Imagine all the people...")

        # THEN
        assert paroles.vecteur is None

    def test_vecteur_peut_etre_defini(self):
        # GIVEN
        embedding = [0.1, 0.2, 0.3]
        paroles = Paroles("Test", vecteur=embedding)

        # WHEN
        result = paroles.vecteur

        # THEN
        assert result == embedding
        assert isinstance(result, list)
