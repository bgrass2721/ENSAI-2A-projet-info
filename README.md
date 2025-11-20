# ENSAI-2A-projet-info

Voici les étapes à suivre pour pouvoir profiter convenablement de notre application.

## : Application à avoir

Il faut utiliser le SSPCloud datalab pour que notre application fonctionne

-  Lancer une instance de [Visual Studio Code], pour ce faire 
  - [ ] aller sur le github de L. Deneuville 
  https://ludo2ne.github.io/ENSAI-2A-Projet-info/doc/tp/tools.html#custom-service
  - [ ] cliquer sur le lien SSPCloud
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [ ] Lancer une instance de [PostgreSQL](https://www.postgresql.org/)


## : Cloner le dépôt

- [ ] Ouvrir VSCode
- [ ] Ouvrir un terminal bash
- [ ] Entrer la commande suivante dans le terminal
  - `git clone https://github.com/bgrass2721/ENSAI-2A-projet-info.git`


### Ouvrir le dossier

- [ ] Fichier > Ouvrir dossier
- [ ] Sélectionner le dossier *ENSAI-2A-PROJET-INFO*


## : Installer les packages requis

- [ ] Dans un terminal Bash, lancer la commande si dessous pour installer les packages

```bash
pip install -r requirements.txt
```

## : Variables d'environnement

Remplir le fichier .env avec les informations fournises dans le README de l'instance Postgresql
que vous avez lancé

- [ ] Create a file called `.env`
- [ ] Paste in and complete the elements below

```default
POSTGRES_HOST = 
POSTGRES_PORT = 
POSTGRES_DATABASE = 
POSTGRES_USER = 
POSTGRES_PASSWORD = 
```


## : Les tests unitaires

Vous pouvez lancer les tests unitaires à l'aide de la commande suivante

- [ ] Dans un terminal: `pytest -v` 

## : Lancer l'API

Pour lancer l'API, il faut lancer la commande ci-dessous dans un terminal

- [ ] `python src/app.py`

Vous pouvez accéder à une visualisation web de notre API en allant dans votre datalab puis en 
cliquant sur le bouton "ouvrir" du service vscode-python puis en cliquant sur "ce lien" situé dans 
la phrase "Vous pouvez vous connecter à votre port personnalisé (5000) en utilisant ce lien"

## : Lancer le client

Cette application fournie une interface graphique simple pour naviguer entre les différents menus.
Pour y accéder:
- [ ] Si c'est le premier démarrage, dans un nouveau terminal, 
  taper la commande suivante : `python start.py`
  - cette commande va réinitialiser la base de donnée et télécharger quelques musiques de bases
  - Attention cette commande prend du temps (3 minutes pour les 30 chansons)
- [ ] Dans un nouveau terminal, taper la commande suivante : `python src/main.py`
- Vous pouvez maintenant utiliser l'application. Voici l'explication des différents menus:
  - Ajouter une musique: permet d'ajouter une musique de votre choix en entrant le titre et 
  l'artiste
  - Créer une playlist: permet de créer une playlist à l'aide d'un thème et d'un nombre de musiques.
  - Catalogue de musiques: permet de consulter les musiques présentes dans la base de donnée
  - Catalogue de playlists: permet de consulter les playlists présentes dans la base de donnée


