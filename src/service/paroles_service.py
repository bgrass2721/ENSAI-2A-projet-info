from business_object.chanson import Chanson
import requests

class ParolesService():

    def add_from_API(chanson: Chanson):
        """
        Recherche les paroles d'une chanson via LRCLIB à partir du titre et de l'artiste.
        Retourne les paroles si trouvées, sinon None.
        """
        # URL de l'API de recherche LRCLIB
        url = "https://lrclib.net/api/get"

        # Paramètres de la requête
        params = {
            "track_name": chanson.titre,
            "artist_name": chanson.artiste
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Si des paroles sont disponibles
            if "plainLyrics" in data and data["plainLyrics"]:
                return data["plainLyrics"]
            else:
                print("Paroles non trouvées pour cette chanson.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return None