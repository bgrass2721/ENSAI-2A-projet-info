import requests
from InquirerPy import prompt

from view.abstract_view import AbstractView


class CreatePlaylistView(AbstractView):
    def __init__(self):
        self.__questions = [
            {
                "type": "input",  # Demande une saisie texte
                "message": "Thème de la playlist : ",
                "name": "nom",  # Nom de la réponse
                "validate": lambda result: len(result) > 2,  # Validation pour ne pas laisser vide
                "invalid_message": "Le thème de la playlist doit faire plus de 2 caractères.",
            },
            {
                "type": "number",
                "message": " Nombre de musique max : ",
                "name": "nbsongs",  # Nom de la réponse
                "validate": lambda result: result.isdigit() and 1 <= int(result),  # Validation pour ne pas laisser vide
                "invalid_message": "Le nombre doit être un entier positif.",
            },
        ]

    def display_info(self):
        print("Veuillez entrer le thème de votre playlist et le nombre de musique maximum")

    def make_choice(self):
        reponses = prompt(self.__questions)
        reponses["nbsongs"]=int(reponses["nbsongs"])
        print(reponses)
        response = requests.post("http://0.0.0.0:5000/playlists", json=reponses)
        if response.status_code == 500:
            print("Echec de la création de la playlist")
            from view.start_view import StartView

            return StartView()
        else:
            from view.playlist_catalog_view import PlaylistDetailView

            return PlaylistDetailView(reponses["nom"])
