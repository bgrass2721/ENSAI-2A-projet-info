from .embedding_service import EmbeddingService
import numpy as np


class RequestEmbeddingService(EmbeddingService):
    """
    Service pour vectoriser les requêtes utilisateur.
    Ajoute la méthode compare() pour comparer des vecteurs.
    """
    
    def compare(self, vecteur1: list, vecteur2: list) -> float:
        """
        Compare deux vecteurs avec la similarité cosinus.
        
        Args:
            vecteur1: Premier vecteur
            vecteur2: Deuxième vecteur
            
        Returns:
            float: Score de similarité entre 0 et 1 (1 = identique)
        """
        try:
            v1 = np.array(vecteur1)
            v2 = np.array(vecteur2)
            
            similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            
            return float(similarity)
            
        except Exception as e:
            print(f"Erreur lors de la comparaison: {str(e)}")
            return None