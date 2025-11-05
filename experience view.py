from InquirerPy import prompt

# Liste des types de Pokémon et des attaques pour l'exemple
list_types = ['Fire', 'Water', 'Electric', 'Grass', 'Rock', 'Psychic']
list_attack_names = ['Tackle', 'Flamethrower', 'Thunderbolt', 'Vine Whip', 'Earthquake', 'Psychic']

def create_pokemon():
    # Affichage d'une bordure avant de commencer le processus de création du Pokémon
    with open("src/graphical_assets/border.txt", "r", encoding="utf-8") as asset:
        print(asset.read())  # Affiche la bordure graphique
        print("\n--- Pokémon Creation ---\n")
    
    def validate_name(val):
        print(f"Validating name: '{val}'")
        if val == '':
            return "Name cannot be empty"
        return True

    # Définition des questions à poser à l'utilisateur
    questions = [
        {
            "type": "input",  # Demande une saisie texte
            "message": "Pokemon name : ",
            "name": "name",  # Nom de la réponse
            "validate": lambda result: len(result) > 0,  # Validation pour ne pas laisser vide
            "invalid_message": "Input cannot be empty.",
        },
        {
            "type": "list",  # Liste déroulante avec options
            "message": "Pokemon type : ",
            "name": "type",  # Nom de la réponse
            "choices": list_types  # Options disponibles
        },
        {
            "type": "number",  # Nombre avec validation
            "message": "Pokemon level : ",
            "name": "level",  # Nom de la réponse
            "min_allowed": 1,  # Minimum
            "max_allowed": 100,  # Maximum
            "validate": lambda val: (1 <= int(val) <= 100) or "Level must be between 1 and 100"
        },
        {
            "type": "checkbox",  # Choix multiple avec cases à cocher
            "message": "Select some attacks (SPACE to select, ENTER to validate) : ",
            "name": "attacks",  # Nom de la réponse
            "choices": list_attack_names,  # Liste d'options
            "validate": lambda selection: len(selection) >= 2,
            "invalid_message": "Select at least 2 toppings.",
        }
    ]

    # Affichage du menu et récupération des réponses
    responses = prompt(questions)
    
    # Affichage d'une bordure après avoir récupéré les réponses
    with open("src/graphical_assets/border.txt", "r", encoding="utf-8") as asset:
        print("\n--- Pokémon Creation Summary ---\n")
        print(asset.read())  # Affiche une autre bordure ou la même après avoir obtenu les réponses

    # Affichage des réponses
    print(f"Name: {responses['name']}")
    print(f"Type: {responses['type']}")
    print(f"Level: {responses['level']}")
    print(f"Attacks: {', '.join(responses['attacks'])}")
    print(responses)

# Lancer la fonction pour créer un Pokémon
if __name__ == "__main__":
    create_pokemon()
