from InquirerPy import prompt

from view.abstract_view import AbstractView


class StartView(AbstractView):
    def __init__(self):
        self.__questions = [
            {
                "type": "list",
                "name": "choix",
                "message": f"Bonjour, que voulez vous faire ?",
                "choices": [
                    "Ajouter une musique",
                    "Créer une playlist",
                    "Catalogue de musiques",
                    "Catalogue de playlists",
                    "Quitter",
                ],
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
            from view.add_song_view import AddSongView

            return AddSongView()

        elif reponse["choix"] == "Créer une playlist":
            from view.create_playlist_view import CreatePlaylistView

            return CreatePlaylistView()

        elif reponse["choix"] == "Catalogue de musiques":
            from view.song_catalog_view import SongCatalogArtist

            return SongCatalogArtist()

        elif reponse["choix"] == "Catalogue de playlists":
            from view.playlist_catalog_view import PlaylistCatalogView

            return PlaylistCatalogView()
