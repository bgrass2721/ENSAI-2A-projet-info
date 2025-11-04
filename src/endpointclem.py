import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from dao.dao import DAO
from utils.log_init import initialiser_logs

app = FastAPI(title="Mon webservice")


initialiser_logs("Webservice")

dao = DAO()


class ParolesModel(BaseModel):
    """Modèle pour les paroles/embeddings, si nécessaire pour l'API."""
    vecteur: List[float] 

class ChansonModel(BaseModel):
    """Modèle pour la Chanson, pour les réponses de l'API."""
    id: Optional[int]
    titre: str
    artiste: str
    annee: Optional[int]
    # Ajout d'une configuration pour gérer les objets non-dict (Chanson)
    class Config:
        orm_mode = True 


class PlaylistModel(BaseModel):
    """Modèle pour la Playlist."""
    # L'id n'est pas un attribut de l'objet Playlist, mais il est retourné par l'insertion dans la BD 
    id_playlist: Optional[int] 
    nom: str

    class Config:
        orm_mode = True

# --- Conversion Business Object -> Pydantic Model ---

def convert_chanson_to_model(chanson) -> ChansonModel:
    """Convertit un objet Chanson en ChansonModel."""
    
    return ChansonModel(
        id=None, 
        titre=chanson.titre,
        artiste=chanson.artiste,
        annee=chanson.annee,
        content_paroles=chanson.paroles.content if chanson.paroles and hasattr(chanson.paroles, 'content') else None
    )

def convert_playlist_to_model(id_playlist: int, playlist) -> PlaylistModel:
    """Convertit un objet Playlist en PlaylistModel avec son ID BD."""
    return PlaylistModel(
        id_playlist=id_playlist,
        nom=playlist.nom,
        chansons=[convert_chanson_to_model(c) for c in playlist.chansons] # Décommenter si nécessaire
    )


# --- Endpoint pour la Consultation des Chansons ---
@app.get("/chansons/", response_model=List[ChansonModel], summary="Retourne la liste complète des chansons disponibles.")
async def get_all_chansons():
    """
    Récupère toutes les chansons du DAO et les convertit en modèles Pydantic.
    """
    try:
        # Appel au DAO pour récupérer les Business Objects (BO)
        liste_chansons_bo = dao.get_chansons() 
    except Exception as e:
        # Gère les erreurs de connexion/exécution de la base de données
        print(f"Erreur DAO lors de la récupération des chansons: {e}")
        raise HTTPException(status_code=500, detail="Une erreur interne est survenue lors de la récupération des chansons.")

    # Conversion des Business Objects en Pydantic Models
    liste_model = [convert_chanson_to_model(chanson) for chanson in liste_chansons_bo]

    return liste_model

class NewChansonInput(BaseModel):
    """Modèle Pydantic pour les données reçues lors d'une requête POST."""
    titre: str
    artiste: str
    annee: Optional[int] = None # L'année est facultative (default None dans Chanson)
    paroles: str

# --- Dans votre fichier API (ex: api.py) ---

@app.post("/chansons/", response_model=ChansonModel, status_code=201, summary="Ajoute une chanson (récupération auto des paroles).")
async def add_chanson_from_api(chanson_data: NewChansonInput):
    """
    Orchestre la création complète d'une chanson :
    1. Instancie la chanson.
    2. Appelle le ParolesService pour récupérer les paroles via une API externe.
    3. Vectorise les paroles (via EmbeddingService).
    4. Sauvegarde la chanson complète dans le DAO.
    """
    try:
        chanson_bo = chanson_service.instantiate_chanson(
            titre=chanson_data.titre, 
            artiste=chanson_data.artiste
        )
        chanson_service.add_annee(chanson_bo, chanson_data.annee) 
        chanson_complete = chanson_service.add_chanson_paroles(chanson_bo)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de la création de la chanson: {e}")

    return convert_chanson_to_model(chanson_complete)

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
