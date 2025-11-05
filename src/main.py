import logging

import dotenv

from utils.log_init import initialiser_logs
from view.start_view import StartView

if __name__ == "__main__":
    # On charge les variables d'envionnement
    dotenv.load_dotenv(override=True)

    initialiser_logs("Application")

    current_view = StartView()
    nb_erreurs = 0

    while current_view:
        if nb_erreurs > 100:
            print("Le programme recense trop d'erreurs et va s'arrêter")
            break
        try:
            # Affichage du menu
            current_view.display_info()

            # Affichage des choix possibles
            current_view = current_view.choisir_menu()
        except Exception as e:
            logging.info(e)
            nb_erreurs += 1
            current_view = StartView()

    # Lorsque l on quitte l application
    print("----------------------------------")
    print("Au revoir")

    logging.info("Fin de l'application")
