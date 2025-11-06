import json
from abc import ABC

import requests


class EmbeddingService(ABC):
    """
    Classe abstraite pour les services d'embedding.
    Fournit la méthode vectorise() commune à toutes les classes dérivées.
    """

    def __init__(self):
        self.OLLAMA_EMBED_URL = "https://llm.lab.sspcloud.fr/ollama/api/embed"
        self.token = "sk-9362a2b2bec045af9dfc896ee3d4e14c"  # Clem
        self.model = "bge-m3"

    def vectorise(self, texte: str) -> list:
        """
        Vectorise un texte via l'API Ollama.

        Args:
            texte: Le texte à vectoriser

        Returns:
            list: Le vecteur embedding ou None en cas d'erreur
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        data = {"model": self.model, "input": texte}

        try:
            response = requests.post(self.OLLAMA_EMBED_URL, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                embedding = response.json().get("embeddings")[0]
                return embedding
            else:
                print(f"Erreur {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"Exception lors de la vectorisation: {str(e)}")
            return None


if __name__ == "__main__":
    text = "bonjour"
    vect = EmbeddingService().vectorise(text)
    print(type(vect))
