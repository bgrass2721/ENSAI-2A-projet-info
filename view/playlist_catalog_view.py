import requests
from InquirerPy import prompt

from view.abstract_view import AbstractView
# Les imports de vues se font dans les méthodes pour éviter les imports circulaires

class PlaylistCatalogView(AbstractView):
    """
    Première vue : Affiche la liste des noms de playlists disponibles.
    """
    def __init__(self):
        self.list_playlist_noms = ["Quitter"]
        
        try:
            # Récupère la liste de toutes les playlists
            response = requests.get("http://127.0.0.1:8000/playlists")
            response.raise_for_status() 
            
            playlists_data = response.json()
            
            # Ajoute les noms des playlists à la liste
            for playlist in playlists_data:
                if 'nom' in playlist:
                    self.list_playlist_noms.append(playlist['nom'])

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des playlists : {e}")
            # La liste ne contiendra que "Quitter"
        
        # Définit la question pour InquirerPy
        self.__questions = [
            {
                "type": "list",
                "message": "Playlists disponibles :",
                "name": "playlist_nom",  # Le nom de la réponse
                "choices": self.list_playlist_noms
            }
        ]

    def display_info(self):
        try:
            with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
                print(asset.read())
        except FileNotFoundError:
            print("--- Mus'IA - Catalogue des Playlists ---")
        print("Veuillez choisir une playlist à inspecter :")


    def make_choice(self):
        from view.start_view import StartView
        
        reponse = prompt(self.__questions)
        choix_nom = reponse.get("playlist_nom")

        if choix_nom == "Quitter" or not choix_nom:
            return StartView()
        
        else: 
            # Transfère vers la vue de détail pour ce nom de playlist
            return PlaylistDetailView(choix_nom)


class PlaylistDetailView(AbstractView):
    """
    Deuxième vue : Affiche les détails (les chansons) d'UNE playlist sélectionnée.
    Inspiré de SongCatalogSong.
    """
    def __init__(self, nom_playlist: str):
        self.nom_playlist = nom_playlist
        self.chansons = []
        
        try:
            # Appelle l'endpoint pour récupérer les chansons de cette playlist
            url = f"http://127.0.0.1:8000/playlists/{self.nom_playlist}/songs"
            response = requests.get(url)
            response.raise_for_status()
            
            self.chansons = response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des chansons pour '{self.nom_playlist}': {e}")
            
        # Question pour "Quitter" (comme dans SongCatalogSong)
        self.__questions = [
            {
                "type": "list",
                "message": "Appuyez sur Entrée pour quitter",
                "name": "action",
                "choices": ["Quitter"],
            }
        ]

    def display_info(self):
        try:
            with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
                print(asset.read())
        except FileNotFoundError:
            print("--- Mus'IA ---")
            
        print(f"\n--- Chansons de la playlist: {self.nom_playlist} ---")
        
        if not self.chansons:
            print("\nCette playlist est vide.")
        else:
            # Affiche les chansons trouvées
            for i, chanson in enumerate(self.chansons, 1):
                titre = chanson.get('titre', 'N/A')
                artiste = chanson.get('artiste', 'N/A')
                annee = chanson.get('annee', 'N/A')
                print(f"  {i}. {titre} - {artiste} ({annee})")
        print("-" * (len(self.nom_playlist) + 32))


    def make_choice(self):
        from view.start_view import StartView
        
        # Pose la question "Quitter"
        prompt(self.__questions)
        
        # Quoi qu'il arrive, retourne au menu principal
        return StartView()