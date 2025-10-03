import json
import requests

def get_embedding(texte):
    """
    Récupère l'embedding d'un texte via l'API Ollama.
    
    Args:
        texte: Le texte à encoder
        
    Returns:
        list: L'embedding ou un message d'erreur
    """
    OLLAMA_EMBED_URL = "https://llm.lab.sspcloud.fr/ollama/api/embed"
    token = "sk-9362a2b2bec045af9dfc896ee3d4e14c"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    data = {"model": "bge-m3", "input": texte}
    
    try:
        response = requests.post(OLLAMA_EMBED_URL, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:    
            embedding = response.json().get("embeddings")[0]    
            print(f"✓ Embedding généré (taille: {len(embedding)})")
            print(f"  Premiers éléments: {embedding[:5]}")
            return embedding
        else:    
            print(f"✗ Erreur {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return None


def test_embeddings():
    """Test la génération d'embeddings pour plusieurs textes."""
    
    print("=" * 60)
    print("TEST DES EMBEDDINGS")
    print("=" * 60)
    
    # Test 1
    print("\n1. Test avec 'j'aime toi'")
    paroles1 = "j'aime toi"
    emb1 = get_embedding(paroles1)
    
    # Test 2
    print("\n2. Test avec 'je t'aime'")
    paroles2 = "je t'aime"
    emb2 = get_embedding(paroles2)
    
    # Test 3 - Texte plus long
    print("\n3. Test avec des paroles plus longues")
    paroles3 = "Dans la nuit étoilée, je chante mes rêves et mes espoirs"
    emb3 = get_embedding(paroles3)
    
    # Comparaison si les embeddings sont valides
    if emb1 and emb2:
        print("\n" + "=" * 60)
        print("COMPARAISON DES EMBEDDINGS")
        print("=" * 60)
        
        # Calcul de similarité cosinus
        import numpy as np
        
        def cosine_similarity(vec1, vec2):
            """Calcule la similarité cosinus entre deux vecteurs."""
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        sim_1_2 = cosine_similarity(emb1, emb2)
        print(f"\nSimilarité entre '{paroles1}' et '{paroles2}': {sim_1_2:.4f}")
        
        if emb3:
            sim_1_3 = cosine_similarity(emb1, emb3)
            sim_2_3 = cosine_similarity(emb2, emb3)
            print(f"Similarité entre '{paroles1}' et '{paroles3}': {sim_1_3:.4f}")
            print(f"Similarité entre '{paroles2}' et '{paroles3}': {sim_2_3:.4f}")
    
    print("\n" + "=" * 60)
    print("FIN DES TESTS")
    print("=" * 60)


if __name__ == "__main__":
    # Vérifier que requests est installé
    try:
        import numpy as np
    except ImportError:
        print("⚠ numpy n'est pas installé. La comparaison des embeddings sera limitée.")
    
    test_embeddings()