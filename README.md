# ENSAI-2A-projet-info

This are the following steps to use our application
## : Application à avoir

You should use the SSPCoud datalab to use our application

- Launch [Visual Studio Code], to do so : 
  - [ ]go on the github of L. Deneuville 
  https://ludo2ne.github.io/ENSAI-2A-Projet-info/doc/tp/tools.html#custom-service
  - [ ] click on the link SSPCloud
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [ ] Launch [PostgreSQL](https://www.postgresql.org/)


## : Clone the repository

- [ ] Open VSCode
- [ ] Open a new terminal
- [ ] Write the following command in this terminal
  - `git clone https://github.com/bgrass2721/ENSAI-2A-projet-info.git`


### Open Folder

- [ ] File > Open Folder
- [ ]  Select folder *ENSAI-2A-PROJET-INFO*


## : Install required packages

- [ ] In Git Bash, run the following command

```bash
pip install -r requirements.txt
```

## : Environment variables

Fill the .env file with the information provided in the README of the PostgreSQL instance you 
launched.

- [ ] Create a file called `.env`
- [ ] Paste in and complete the elements below

```default
POSTGRES_HOST = 
POSTGRES_PORT = 
POSTGRES_DATABASE = 
POSTGRES_USER = 
POSTGRES_PASSWORD = 
```


## : Unit tests

You can run the unit tests with this command

- [ ] in a terminal: `pytest -v` 

## : Launching the API

To launch the API, run the command below in a terminal:

- [ ] `python src/app.py`

You can access a web visualization of the API by going to your datalab, clicking the **“open”** 
button of the *vscode-python* service, then clicking on **“this link”** in the sentence:  
“You can connect to your custom port (5000) using this link.”

## : Launching the Client

This application provides a simple graphical interface to navigate between the different menus.  
To access it:

- [ ] If this is the first startup, in a new terminal, run the following command:  
  `python start.py`  
  - This command resets the database and downloads some basic songs.  
  - Note: this operation takes time (about 3 minutes for 30 songs).

- [ ] In a new terminal, run:  
  `python src/main.py`

You can now use the application. Here is an explanation of the different menus:

- **Add a song**: allows you to add a song by entering its title and artist.  
- **Create a playlist**: allows you to create a playlist using a theme and a number of songs.  
- **Song catalog**: lets you view the songs available in the database.  
- **Playlist catalog**: lets you view the playlists available in the database.
"""


