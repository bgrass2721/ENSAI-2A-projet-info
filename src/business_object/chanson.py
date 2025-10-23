from .paroles import Paroles  # Import de la classe Paroles définie dans le même package


class Chanson:
    """
    Classe représentant une chanson dans Mus'IA.

    Attributs
    ---------
    id : int
        Identifiant unique de la chanson.
    titre : str
        Titre de la chanson.
    artiste : str
        Nom de l'artiste ou du groupe.
    annee : int ou None
        Année de sortie de la chanson. Par défaut None.
    paroles : Paroles ou None
        Objet Paroles associé à la chanson. Par défaut None.

    Méthodes
    --------
    afficher() -> str
        Retourne une représentation textuelle de la chanson.

    Exemple
    -------
    >>> p = Paroles("Imagine there's no heaven...")
    >>> c = Chanson(1, "Imagine", "John Lennon", 1971, p)
    >>> print(c.afficher())
    Imagine - John Lennon (1971)
    """

    def __init__(self, id: int, titre: str, artiste: str, annee: int = None, paroles: Paroles = None):
        self.id = id
        self.titre = titre
        self.artiste = artiste
        self.annee = annee
        self.paroles = paroles

    def afficher(self) -> str:
        """
        Retourne une représentation textuelle de la chanson.

        Retour
        ------
        str
            "Titre - Artiste (Année)" si l’année est connue,
            sinon "Titre - Artiste".
        """
        if self.annee:
            return f"{self.titre} - {self.artiste} ({self.annee})"
        return f"{self.titre} - {self.artiste}"

