import requests
from InquirerPy import prompt

from view.abstract_view import AbstractView


class SongCatalogArtist(AbstractView):
    def __init__(self):
        allsongs = requests.get("http://0.0.0.0:5000/chansons/").json()
        songs = ["Quitter"]
        for song in allsongs:
            if song["artiste"] not in songs:
                songs.append(song["artiste"])

        self.__questions = [
            {
                "type": "list",  # Liste déroulante avec options
                "message": "Noms des artistes",
                "name": "artiste",  # Nom de la réponse
                "choices": songs,  # Options disponibles
            }
        ]

    def display_info(self):
        print("Veuillez choisir l'artiste")

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["artiste"] == "Quitter":
            from view.start_view import StartView

            return StartView()

        else:
            return SongCatalogTitle(reponse["artiste"])


class SongCatalogTitle(AbstractView):
    def __init__(self, artiste):
        self.__artiste = artiste
        allsongs = requests.get("http://0.0.0.0:5000/chansons/").json()
        songs = ["Quitter"]
        for song in allsongs:
            if song["artiste"] == artiste:
                songs.append(song["titre"])

        self.__questions = [
            {
                "type": "list",  # Liste déroulante avec options
                "message": "Titres des musiques",
                "name": "titre",  # Nom de la réponse
                "choices": songs,  # Options disponibles
            }
        ]

    def display_info(self):
        print("Veuillez choisir le titre")

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["titre"] == "Quitter":
            from view.start_view import StartView

            return StartView()

        else:
            return SongCatalogSong(self.__artiste, reponse["titre"])


class SongCatalogSong(AbstractView):
    def __init__(self, artiste, titre):
        self.__song = requests.get(
            "http://0.0.0.0:5000/chansons/search", params={"titre": titre, "artiste": artiste}
        ).json()
        choice = ["Quitter"]

        self.__questions = [
            {
                "type": "list",  # Liste déroulante avec options
                "message": "",
                "name": "artiste",  # Nom de la réponse
                "choices": choice,  # Options disponibles
            }
        ]

    def display_info(self):
        print(f"""
        Titre: {self.__song["titre"]}
        
        Artiste: {self.__song["artiste"]}

        Paroles:
        {self.__song["paroles"]["content"]}
        """)

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse["artiste"] == "Quitter":
            from view.start_view import StartView

            return StartView()

        else:
            return StartView()
