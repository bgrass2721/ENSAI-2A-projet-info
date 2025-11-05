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
