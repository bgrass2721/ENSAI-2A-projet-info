from InquirerPy import prompt

from view.abstract_view import AbstractView


class StartView(AbstractView):
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
            "validate": lambda result: result > 0,  # Validation pour ne pas laisser vide
            "invalid_message": "Le nombre doit être positif.",
        }
        ]
    def display_info(self):
        with open("src/graphical_assets/banner.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        print("Veuillez entrer le thème de votre playlist et le nombre de musique maximun(un entier)")

    def make_choice(self):
        reponses = prompt(self.__questions)
        response = requests.get("http://127.0.0.1:8000/playlists", params=responses)
        if response.status_code == 500:
            print("Je sais pas pourquoi ca voudrait pas (faudra qu'on regarde)")
        else:
            print("La playlist est créée!")

        from view.start_view import StartView
        return StartView()
