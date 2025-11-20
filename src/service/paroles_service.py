import requests

from business_object.chanson import Chanson
from business_object.paroles import Paroles


class ParolesService:
    def add_from_API(self, chanson):
        """
        Recherche les paroles d'une chanson via LRCLIB à partir du titre et de l'artiste.
        Retourne les paroles si trouvées, sinon None.
        """
        # URL de l'API de recherche LRCLIB
        url = "https://lrclib.net/api/get"

        # Paramètres de la requête
        params = {"track_name": chanson.titre, "artist_name": chanson.artiste}

        try:
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            # Si des paroles sont disponibles
            if "plainLyrics" in data and data["plainLyrics"]:
                return Paroles(data["plainLyrics"])
            else:
                print("Paroles non trouvées pour cette chanson.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return None


if __name__ == "__main__":
    test_chanson_1 = Chanson("Imagine", "John Lennon")
    paroles = ParolesService().add_from_API(test_chanson_1)
    print(paroles.content)

    test_chanson_2 = Chanson("blablabla", "jsp")
    paroles = ParolesService().add_from_API(test_chanson_2)
    print(paroles)
