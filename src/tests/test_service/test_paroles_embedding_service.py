import pytest
from src.service.paroles_embedding_service import ParolesEmbeddingService


class TestParolesEmbeddingService:
    """Tests pour ParolesEmbeddingService."""
    
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return ParolesEmbeddingService()
    
    def test_vectorise_paroles_simples(self, service):
        """Test vectorisation de paroles simples."""
        paroles = "Dans la nuit étoilée, je chante mes rêves"
        vecteur = service.vectorise(paroles)
        
        assert vecteur is not None, "Le vecteur ne doit pas être None"
        assert isinstance(vecteur, list), "Le vecteur doit être une liste"
        assert len(vecteur) > 0, "Le vecteur ne doit pas être vide"
        assert len(vecteur) == 1024, "La dimension devrait être 1024 pour bge-m3"
        
        print(f"\n✓ Paroles vectorisées: {paroles}")
        print(f"  Dimension: {len(vecteur)}")
        print(f"  Premiers éléments: {vecteur[:5]}")
    
    def test_vectorise_paroles_longues(self, service):
        """Test vectorisation de paroles longues."""
        paroles = """
        Je marche seul dans la rue
        Sous la pluie qui tombe
        Je pense à toi mon amour
        Et à tous nos souvenirs
        """
        vecteur = service.vectorise(paroles)
        
        assert vecteur is not None, "Le vecteur ne doit pas être None"
        assert len(vecteur) == 1024, "La dimension devrait être 1024"
        
        print(f"\n✓ Paroles longues vectorisées")
        print(f"  Dimension: {len(vecteur)}")
    
    def test_vectorise_paroles_courtes(self, service):
        """Test vectorisation de paroles très courtes."""
        paroles = "Amour"
        vecteur = service.vectorise(paroles)
        
        assert vecteur is not None, "Le vecteur ne doit pas être None"
        assert len(vecteur) == 1024, "La dimension devrait être 1024"
        
        print(f"\n✓ Mot unique vectorisé: {paroles}")
    
    def test_vectorise_paroles_vides(self, service):
        """Test vectorisation de paroles vides."""
        paroles = ""
        vecteur = service.vectorise(paroles)
        
        # Comportement attendu : peut retourner None ou un vecteur
        # À adapter selon votre API
        if vecteur is not None:
            assert isinstance(vecteur, list), "Le vecteur doit être une liste"
        
        print(f"\n✓ Paroles vides gérées")
    
    def test_vectorise_paroles_avec_caracteres_speciaux(self, service):
        """Test vectorisation avec caractères spéciaux."""
        paroles = "C'est l'été ! Où es-tu ? 🎵"
        vecteur = service.vectorise(paroles)
        
        assert vecteur is not None, "Le vecteur ne doit pas être None"
        assert len(vecteur) == 1024, "La dimension devrait être 1024"
        
        print(f"\n✓ Caractères spéciaux gérés: {paroles}")