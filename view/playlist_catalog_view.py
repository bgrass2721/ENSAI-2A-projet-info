from InquirerPy import prompt

from view.abstract_view import AbstractView


class PlaylistCatalogView(AbstractView):
    def __init__(self):
        playlists = requests.get("http://127.0.0.1:8000/playlists")
        list_playlist= ["Quitter"]
        for playlist in playlists:
            list_playlist.append(playlist.nom)

        self.__questions = [
            {
            "type": "list",  # Liste déroulante avec options
            "message": "Playlist disponible :",
            "name": "playlist",  # Nom de la réponse
            "choices": list_playlist  # Options disponibles
            }
        ]

    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["choix"] == "Quitter":
            pass
        else: 
            responses = requests.get("http://127.0.0.1:8000/playlists", json=responses)
            print()
