class Chanson:
    """
    Classe représentant une chanson dans l'application Mus'IA.

    Attributs
    ---------
    id : int
        Identifiant unique de la chanson.
    titre : str
        Titre de la chanson.
    artiste : str
        Nom de l'artiste ou du groupe.
    annee : int
        Année de sortie de la chanson.
    paroles : str
        Paroles de la chanson.

    Méthodes
    --------
    afficher() -> str
        Retourne une représentation textuelle de la chanson.
    """

    def __init__(self, id: int, titre: str, artiste: str, annee: int, paroles: str = None):
        self.id = id
        self.titre = titre
        self.artiste = artiste
        self.annee = annee
        self.paroles = paroles

    def afficher(self) -> str:
        """
        Retourne une chaîne lisible représentant la chanson.

        Retour
        ------
        str
            Représentation textuelle au format :
            "Titre - Artiste (Année)"
        """
        return f"{self.titre} - {self.artiste} ({self.annee})"
