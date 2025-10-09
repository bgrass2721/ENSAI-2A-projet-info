"""
Module paroles.py
Contient la classe Paroles utilisée dans le système Mus'IA.
"""

class Paroles:
    """
    Classe représentant les paroles d'une chanson dans le système Mus'IA.

    Attributs
    ---------
    content : str
        Contenu textuel des paroles.
    vecteur : list[float] ou None
        Représentation vectorielle (embedding) des paroles. Par défaut None.

    Méthodes
    --------
    afficher() -> str
        Retourne le texte complet des paroles.

    Exemple
    -------
    >>> p = Paroles("Here comes the sun...")
    >>> print(p.afficher())
    Here comes the sun...
    """

    def __init__(self, content: str, vecteur: list = None):
        self.content = content
        self.vecteur = vecteur

    def afficher(self) -> str:
        """
        Affiche le texte complet des paroles.

        Retour
        ------
        str
            Texte brut des paroles.
        """
        return self.content
