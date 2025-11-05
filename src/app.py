import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# -------------------------------------------------------------------
#  Import de la couche Client (selon le diagramme)
# (Assurez-vous que ces chemins d'import sont corrects)
# -------------------------------------------------------------------
from client.playlist_client import PlaylistClient
from client.chanson_client import ChansonClient

# -------------------------------------------------------------------
#  Import de l'outil d'initialisation des logs
# -------------------------------------------------------------------
from utils.log_init import initialiser_logs


# -------------------------------------------------------------------
#  Création et configuration de l’application FastAPI
# -------------------------------------------------------------------
app = FastAPI(title="API Mus’IA - Gestion des Playlists")
initialiser_logs("Webservice Mus’IA")

# -------------------------------------------------------------------
#  Instanciation des Clients (au lieu des DAOs)
# -------------------------------------------------------------------
playlist_client = PlaylistClient()
chanson_client = ChansonClient()


# -------------------------------------------------------------------
#  Définition des modèles Pydantic
# (Ces modèles définissent le contrat de l'API, ils restent inchangés)
# -------------------------------------------------------------------

class ParolesModel(BaseModel):
    """Modèle de représentation des paroles et du vecteur d'embedding."""
    vecteur: List[float]
    content: Optional[str] = None


class ChansonModel(BaseModel):
    """Modèle de représentation d’une chanson."""
    titre: str
    artiste: str
    annee: Optional[int]
    paroles: Optional[ParolesModel]

    class Config:
        orm_mode = True


class PlaylistModel(BaseModel):
    """Modèle de représentation d’une playlist."""
    id_playlist: Optional[int]
    nom: str
    chansons: Optional[List[ChansonModel]]

    class Config:
        orm_mode = True


class PlaylistCreationModel(BaseModel):
    """Modèle d'entrée pour la création d'une playlist."""
    nom: str
    keyword: str
    nbsongs: int


class NewChansonInput(BaseModel):
    """Modèle Pydantic pour les données reçues lors d'un POST sur /chansons/."""
    titre: str
    artiste: str
    annee: Optional[int] = None
    paroles: str # Note: Le code original impliquait une recherche de paroles.
                 # Ce modèle implique que les paroles sont fournies.
                 # Le client devra gérer cette logique.

class ParolesContentModel(BaseModel):
    """Modèle pour le retour des paroles simples."""
    titre: str
    artiste: str
    paroles: str


# -------------------------------------------------------------------
#  Redirection automatique vers la documentation interactive
# -------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige l’utilisateur vers la page de documentation (Swagger UI)."""
    return RedirectResponse(url="/docs")


# ===================================================================
#  SECTION : ENDPOINTS POUR LES PLAYLISTS
# ===================================================================

@app.post("/playlists", response_model=PlaylistModel, tags=["Playlists"])
async def create_playlist(data: PlaylistCreationModel):
    """
    Crée une playlist en appelant le client.
    Le client gère la logique de recherche de chansons et de création.
    """
    try:
        # [cite_start]On appelle le client [cite: 51]
        # [cite_start]Note: La méthode 'request_playlist' du diagramme [cite: 51] (str, int)
        # est adaptée pour correspondre au modèle 'PlaylistCreationModel'
        nouvelle_playlist = playlist_client.request_playlist(
            nom=data.nom,
            keyword=data.keyword,
            nbsongs=data.nbsongs
        )
        return nouvelle_playlist
    except Exception as e:
        logging.error(f"Erreur lors de la création de la playlist via client : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {e}")


@app.get("/playlists", response_model=List[PlaylistModel], tags=["Playlists"])
async def get_all_playlists():
    """
    Récupère la liste de toutes les playlists via le client.
    """
    try:
        [cite_start]playlists = playlist_client.get_playlists() # Conforme au diagramme [cite: 51]
        return playlists
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des playlists via client : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.get("/playlists/{id_playlist}", response_model=PlaylistModel, tags=["Playlists"])
async def get_playlist_by_id(id_playlist: int):
    """
    Récupère une playlist spécifique par son ID via le client.
    """
    try:
        [cite_start]playlist = playlist_client.get_playlist(id_playlist) # Conforme au diagramme [cite: 51]
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist introuvable.")
        return playlist
    except HTTPException as he:
        raise he # Transférer l'erreur 404
    except Exception as e:
        logging.error(f"Erreur récupération playlist {id_playlist} via client : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.get("/playlists/{id_playlist}/songs", response_model=List[ChansonModel], tags=["Playlists"])
async def get_songs_from_playlist(id_playlist: int):
    """
    Retourne toutes les chansons d'une playlist via le client.
    """
    try:
        [cite_start]chansons = playlist_client.get_playlist_chansons(id_playlist) # Conforme au diagramme [cite: 51]
        
        # Le client doit renvoyer 'None' ou lever une erreur si la playlist n'existe pas
        if chansons is None:
            raise HTTPException(status_code=404, detail="Playlist introuvable.")
        return chansons
    except HTTPException as he:
        raise he # Transférer l'erreur 404
    except Exception as e:
        logging.error(f"Erreur récupération chansons de playlist {id_playlist} via client : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


# ===================================================================
#  SECTION : ENDPOINTS POUR LES CHANSONS
# ===================================================================

@app.get("/chansons/", response_model=List[ChansonModel], summary="Retourne la liste complète des chansons disponibles.")
async def get_all_chansons():
    """
    Récupère toutes les chansons via le client.
    """
    try:
        [cite_start]liste_chansons = chanson_client.get_chansons() # Conforme au diagramme [cite: 48]
        return liste_chansons
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des chansons via client: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.post("/chansons/", response_model=ChansonModel, status_code=201, summary="Ajoute une chanson.")
async def add_chanson_from_api(chanson_data: NewChansonInput):
    """
    Orchestre la création d'une chanson via le client.
    """
    try:
        # [cite_start]Le client 'add_new_chanson' [cite: 48] est supposé accepter le modèle
        chanson_complete = chanson_client.add_new_chanson(chanson_data)
        return chanson_complete
    except Exception as e:
        logging.error(f"Échec de la création de la chanson via client: {e}")
        raise HTTPException(status_code=500, detail=f"Échec de la création de la chanson: {e}")


@app.get("/chansons/{chanson_id}", response_model=ChansonModel, summary="Fournit les infos d'une chanson par son ID.")
async def get_chanson_by_id(
    chanson_id: int = Path(..., title="L'ID de la chanson à récupérer", ge=1)
):
    """
    Récupère une chanson spécifique par son ID via le client.
    """
    try:
        # [cite_start]Note: Le diagramme [cite: 48] montre get_chanson(str, str).
        # L'endpoint utilise un 'int'. Le client doit exposer
        # une méthode 'get_chanson_by_id(int)' pour correspondre à l'API.
        chanson = chanson_client.get_chanson_by_id(chanson_id)
        
        if not chanson:
            raise HTTPException(
                status_code=404, 
                detail=f"La chanson avec l'ID {chanson_id} n'a pas été trouvée."
            )
        return chanson
    except HTTPException as he:
        raise he # Transférer l'erreur 404
    except Exception as e:
        logging.error(f"Erreur récupération chanson {chanson_id} via client: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.get("/chansons/{chanson_id}/lyrics", response_model=ParolesContentModel, summary="Retourne le texte des paroles d'une chanson.")
async def get_lyrics_for_song(
    chanson_id: int = Path(..., title="L'ID de la chanson", ge=1)
):
    """
    Récupère le texte des paroles d'une chanson via le client.
    """
    try:
        # [cite_start]Note: Le ChansonClient [cite: 46] n'a pas de méthode 'get_lyrics'
        # dans le diagramme. Nous supposons qu'elle existe pour
        # répondre à la contrainte de l'API.
        paroles = chanson_client.get_lyrics_by_chanson_id(chanson_id)

        if not paroles:
            raise HTTPException(
                status_code=404, 
                detail=f"Le contenu des paroles n'est pas disponible pour la chanson ID {chanson_id}."
            )
        return paroles
    except HTTPException as he:
        raise he # Transférer l'erreur 404
    except Exception as e:
        logging.error(f"Erreur récupération paroles {chanson_id} via client: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


# --- Lancement de l'application ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9876)
    logging.info("Arret du Webservice")
