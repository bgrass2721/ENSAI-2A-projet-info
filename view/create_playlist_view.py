from InquirerPy import prompt
import requests
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
            "type": "number",  # Demande une saisie texte
            "message": " Nombre de musique max : ",
            "name": "nbsongs",  # Nom de la réponse
            "validate": lambda result: result > 0 and isinstance(result, int),  # Validation pour ne pas laisser vide
            "invalid_message": "Le nombre doit être un entier positif.",
        }
        ]
    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        print("Veuillez entrer le thème de votre playlist et le nombre de musique maximum")

    def make_choice(self):
        reponses = prompt(self.__questions)
        response = requests.post("http://127.0.0.1:8000/playlists", params=reponses)
        if response.status_code == 500:
            print("Echec de la création de la playlist")
            from view.start_view import StartView
            return StartView()
        else:
            from view.playlist_catalog_view import #à définir
            return #à définir 

        
