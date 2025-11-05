from InquirerPy import prompt

from view.abstract_view import AbstractView


class AddSongView(AbstractView):
    def __init__(self):
        self.__questions = [
            {
            "type": "input",  # Demande une saisie texte
            "message": "Nom du titre : ",
            "name": "name",  # Nom de la réponse
            "validate": lambda result: len(result) > 0,  # Validation pour ne pas laisser vide
            "invalid_message": "Le nom du titre ne peut pas être vide.",
        },
        {
            "type": "input",  # Demande une saisie texte
            "message": "Nom de l'artiste : ",
            "name": "name",  # Nom de la réponse
            "validate": lambda result: len(result) > 0,  # Validation pour ne pas laisser vide
            "invalid_message": "Le nom de l'artiste ne peut pas être vide.",
        }
        ]

    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["choix"] == "Quitter":
            pass

        elif reponse["choix"] == "Ajouter une musique":
            from view.connection_view import ConnectionView

            return ConnectionView()

        elif reponse["choix"] == "Créer une playlist":
            from view.battle_view import BattleView

            return BattleView()

        elif reponse["choix"] == "Catalogue de musiques":
            from view.pokemon_list_view import PokemonListView

            return PokemonListView()

        elif reponse["choix"] == "Catalogue de playlists":
            from view.attack_list_view import AttackListView

            return AttackListView()
