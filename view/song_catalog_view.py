import requests
from InquirerPy import prompt

from view.abstract_view import AbstractView


class SongCatalogArtist(AbstractView):
    def __init__(self):
        allsongs = requests.get("http://127.0.0.1:8000/chansons/")
        songs = ["Quitter"]
        for song in allsongs:
            if song.artiste not in songs:
                songs.append(song.artiste)

        __questions = [
            {
                "type": "list",  # Liste déroulante avec options
                "message": "Noms des artistes",
                "name": "artiste",  # Nom de la réponse
                "choices": songs,  # Options disponibles
            }
        ]

    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        print("Veuillez choisir l'artiste")

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["choices"] == "Quitter":
            from view.start_view import StartView

            return StartView()

        else:
            return SongCatalogArtist(reponse["choices"])


class SongCatalogTitle(AbstractView):
    def __init__(self, artiste):
        __artiste = artiste
        allsongs = requests.get("http://127.0.0.1:8000/chansons/")
        songs = ["Quitter"]
        for song in allsongs:
            if song.artiste == artiste:
                songs.append(song.titre)

        __questions = [
            {
                "type": "list",  # Liste déroulante avec options
                "message": "Titres des musiques",
                "name": "artiste",  # Nom de la réponse
                "choices": songs,  # Options disponibles
            }
        ]

    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        print("Veuillez choisir le titre")

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["choices"] == "Quitter":
            from view.start_view import StartView

            return StartView()

        else:
            return SongCatalogSong(self.artiste, reponse["choices"])


class SongCatalogSong(AbstractView):
    def __init__(self, artiste, titre):
        __song = requests.get(
            "http://127.0.0.1:8000/chansons/", params={titre: titre, artiste: artiste}
        )
        choice = ["Quitter"]

        __questions = [
            {
                "type": "list",  # Liste déroulante avec options
                "name": "artiste",  # Nom de la réponse
                "choices": choice,  # Options disponibles
            }
        ]

    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        print(f"""
        Titre: {self.song.titre}
        
        Artiste: {self.song.artiste}

        Année: {self.song.annee}

        Paroles:
        {self.song.paroles.content}
        """)

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["artiste"] == "Quitter":
            from view.start_view import StartView

            return StartView()

        else:
            return StartView()
