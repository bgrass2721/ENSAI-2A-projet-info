import pytest
import numpy as np
from service.request_embedding_service import RequestEmbeddingService


class TestRequestEmbeddingService:
    """Tests pour RequestEmbeddingService."""
    
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return RequestEmbeddingService()
    
    def test_vectorise_requete_simple(self, service):
        """Test vectorisation d'une requête simple."""
        requete = "Trouve-moi des chansons d'amour"
        vecteur = service.vectorise(requete)
        
        assert vecteur is not None, "Le vecteur ne doit pas être None"
        assert isinstance(vecteur, list), "Le vecteur doit être une liste"
        assert len(vecteur) == 1024, "La dimension devrait être 1024"
        
        print(f"\n✓ Requête vectorisée: {requete}")
        print(f"  Dimension: {len(vecteur)}")
    
    def test_vectorise_requete_complexe(self, service):
        """Test vectorisation d'une requête complexe."""
        requete = "Je cherche de la musique rock des années 80 avec des guitares électriques"
        vecteur = service.vectorise(requete)
        
        assert vecteur is not None, "Le vecteur ne doit pas être None"
        assert len(vecteur) == 1024, "La dimension devrait être 1024"
        
        print(f"\n✓ Requête complexe vectorisée")
    
    def test_compare_vecteurs_identiques(self, service):
        """Test comparaison de vecteurs identiques."""
        texte = "chanson d'amour"
        vecteur1 = service.vectorise(texte)
        vecteur2 = service.vectorise(texte)
        
        similarity = service.compare(vecteur1, vecteur2)
        
        assert similarity is not None, "La similarité ne doit pas être None"
        assert 0.99 <= similarity <= 1.01, "Vecteurs identiques doivent avoir similarité ~1.0"
        
        print(f"\n✓ Vecteurs identiques: similarité = {similarity:.4f}")
    
    def test_compare_vecteurs_similaires(self, service):
        """Test comparaison de vecteurs similaires."""
        texte1 = "chanson d'amour romantique"
        texte2 = "musique romantique et douce"
        
        vecteur1 = service.vectorise(texte1)
        vecteur2 = service.vectorise(texte2)
        
        similarity = service.compare(vecteur1, vecteur2)
        
        assert similarity is not None, "La similarité ne doit pas être None"
        assert 0.0 <= similarity <= 1.0, "La similarité doit être entre 0 et 1"
        assert similarity > 0.5, "Textes similaires devraient avoir similarité > 0.5"
        
        print(f"\n✓ Textes similaires: similarité = {similarity:.4f}")
        print(f"  Texte 1: {texte1}")
        print(f"  Texte 2: {texte2}")
    
    def test_compare_vecteurs_differents(self, service):
        """Test comparaison de vecteurs différents."""
        texte1 = "chanson d'amour romantique"
        texte2 = "rock métal agressif"
        
        vecteur1 = service.vectorise(texte1)
        vecteur2 = service.vectorise(texte2)
        
        similarity = service.compare(vecteur1, vecteur2)
        
        assert similarity is not None, "La similarité ne doit pas être None"
        assert 0.0 <= similarity <= 1.0, "La similarité doit être entre 0 et 1"
        # Textes très différents devraient avoir une similarité plus faible
        
        print(f"\n✓ Textes différents: similarité = {similarity:.4f}")
        print(f"  Texte 1: {texte1}")
        print(f"  Texte 2: {texte2}")
    
    def test_compare_vecteurs_invalides(self, service):
        """Test comparaison avec vecteurs invalides."""
        vecteur1 = [1, 2, 3]
        vecteur2 = [4, 5, 6]
        
        # Devrait gérer les erreurs gracieusement
        similarity = service.compare(vecteur1, vecteur2)
        
        # Soit retourne un résultat, soit None en cas d'erreur
        if similarity is not None:
            assert 0.0 <= similarity <= 1.0, "La similarité doit être entre 0 et 1"
        
        print(f"\n✓ Gestion des vecteurs invalides testée")
    
    def test_compare_symetrie(self, service):
        """Test que compare(A, B) == compare(B, A)."""
        texte1 = "musique classique"
        texte2 = "jazz moderne"
        
        vecteur1 = service.vectorise(texte1)
        vecteur2 = service.vectorise(texte2)
        
        similarity_1_2 = service.compare(vecteur1, vecteur2)
        similarity_2_1 = service.compare(vecteur2, vecteur1)
        
        assert abs(similarity_1_2 - similarity_2_1) < 0.0001, "La comparaison doit être symétrique"
        
        print(f"\n✓ Symétrie vérifiée: {similarity_1_2:.4f} = {similarity_2_1:.4f}")