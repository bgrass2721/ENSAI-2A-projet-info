from .chanson import Chanson  # Import de la classe Chanson


class Playlist:
    """
    Classe représentant une playlist musicale dans Mus'IA.

    Attributs
    ---------
    id : int
        Identifiant unique de la playlist.
    nom : str
        Nom attribué à la playlist.
    chansons : list[Chanson]
        Liste des chansons contenues dans la playlist.

    Méthodes
    --------
    afficher() -> str
        Retourne une représentation textuelle complète de la playlist.
    get_chansons() -> list[Chanson]
        Retourne la liste des chansons contenues dans la playlist.

    Exemple
    -------
    >>> from business_layer.chanson import Chanson
    >>> p = Playlist(1, "Classiques")
    >>> c = Chanson(1, "Imagine", "John Lennon", 1971)
    >>> p.chansons.append(c)
    >>> print(p.afficher())
    Playlist 'Classiques' :
      1. Imagine - John Lennon (1971)
    """

    def __init__(self, id: int, nom: str, chansons: list[Chanson] = None):
        self.id = id
        self.nom = nom
        self.chansons = chansons if chansons is not None else []

    def afficher(self) -> str:
        """
        Retourne une représentation textuelle complète de la playlist.

        Retour
        ------
        str
            Liste formatée contenant toutes les chansons de la playlist.
        """
        if not self.chansons:
            return f"Playlist '{self.nom}' (vide)"
        texte = [f"Playlist '{self.nom}' :"]
        for i, chanson in enumerate(self.chansons, start=1):
            texte.append(f"  {i}. {chanson.afficher()}")
        return "\n".join(texte)

    def get_chansons(self) -> list[Chanson]:
        """
        Retourne la liste des chansons contenues dans la playlist.

        Retour
        ------
        list[Chanson]
            Liste d'objets Chanson.
        """
        return self.chansons
