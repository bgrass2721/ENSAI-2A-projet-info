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
            response = requests.get("http://0.0.0.0:5000/playlists")
            response.raise_for_status() 
            
            playlists_data = response.json()
            
            # Ajoute les noms des playlists à la liste
            for playlist in playlists_data:
                if playlist['nom'] not in playlist:
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
        print("--- Mus'IA - Catalogue des Playlists ---")
        print("Veuillez choisir une playlist à inspecter :")


    def make_choice(self):
        from view.start_view import StartView
        
        reponse = prompt(self.__questions)
        choix_nom = reponse["playlist_nom"]

        if choix_nom == "Quitter":
            return StartView()
        
        else:
            return PlaylistDetailView(choix_nom)


class PlaylistDetailView(AbstractView):
    """
    Deuxième vue : Affiche les détails (les chansons) d'UNE playlist sélectionnée.
    Inspiré de SongCatalogSong.
    """
    def __init__(self, nom_playlist: str):
        self.nom_playlist = nom_playlist
        self.chansons = ["Quitter"]
        
        try:
            # Appelle l'endpoint pour récupérer les chansons de cette playlist
            url = f"http://0.0.0.0:5000/playlists/{self.nom_playlist}/songs"
            response = requests.get(url)
            response.raise_for_status()
            
            chansons = response.json()
            for song in chansons:
                self.chansons.append(song["artiste"]+" | "+song["titre"])
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des chansons pour '{self.nom_playlist}': {e}")
            
        # Question pour "Quitter" (comme dans SongCatalogSong)
        self.__questions = [
            {
                "type": "list",
                "message": "Appuyez sur Entrée pour quitter",
                "name": "action",
                "choices": self.chansons,
            }
        ]

    def display_info(self):         
        print(f"\n--- Chansons de la playlist: {self.nom_playlist} ---")


    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["action"] == "Quitter":
            from view.start_view import StartView
            return StartView()
        else:
            artiste, titre = reponse["action"].split(" | ", 1)
            from view.song_catalog_view import SongCatalogSong
            return SongCatalogSong(artiste,titre)