from InquirerPy import prompt
import requests
from view.abstract_view import AbstractView


class AddSongView(AbstractView):
    def __init__(self):
        self.__questions = [
            {
            "type": "input",  # Demande une saisie texte
            "message": "Nom du titre",
            "name": "titre",  # Nom de la réponse
            "validate": lambda result: len(result) > 0,  # Validation pour ne pas laisser vide
            "invalid_message": "Le nom du titre ne peut pas être vide.",
        },
        {
            "type": "input",  # Demande une saisie texte
            "message": "Nom de l'artiste : ",
            "name": "artiste",  # Nom de la réponse
            "validate": lambda result: len(result) > 0,  # Validation pour ne pas laisser vide
            "invalid_message": "Le nom de l'artiste ne peut pas être vide.",
        }
        ]

    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        print("Veuillez entrer le titre et l'artiste sans faute d'orthographe")

    def make_choice(self):
        reponses = prompt(self.__questions)
        response = requests.get("http://127.0.0.1:8000/chansons", params=responses)
        if response.status_code == 500:
            print("La musique est introuvable")
        else:
            print("La musique est dans la base de donnée")

        from view.start_view import StartView
        return StartView()