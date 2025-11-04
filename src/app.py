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
    # Le vecteur est le champ clé dans la BD, nous l'utilisons pour l'identifier
    vecteur: List[float] # Le vecteur d'embedding

class ChansonModel(BaseModel):
    """Modèle pour la Chanson, pour les réponses de l'API."""
    id: Optional[int] # L'id dans la classe Chanson est présent dans le diagramme 
    titre: str
    artiste: str
    annee: Optional[int]
    # L'objet Paroles est complexe, mais nous allons exposer un minimum d'info, 
    # l'API Client interagit avec les méthodes du DAO pour la création
    # Ajout d'une configuration pour gérer les objets non-dict (Chanson)
    class Config:
        orm_mode = True # ou from_attributes = True pour Python >= 3.11


class PlaylistModel(BaseModel):
    """Modèle pour la Playlist."""
    # L'id n'est pas un attribut de l'objet Playlist, mais il est retourné par l'insertion dans la BD
    id_playlist: Optional[int] 
    nom: str
    
    # La liste des chansons est un attribut de la Playlist 

    class Config:
        orm_mode = True

# --- Fonctions utilitaires (Conversion Business Object -> Pydantic Model) ---

def convert_chanson_to_model(chanson) -> ChansonModel:
    """Convertit un objet Chanson en ChansonModel."""
    
    return ChansonModel(
        # Simplement pour que ça fonctionne sans modification majeure de Chanson
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

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
