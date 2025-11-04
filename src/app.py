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
    # Si nous voulions exposer les paroles complètes, on utiliserait le content:
    # content_paroles: Optional[str]

    # Ajout d'une configuration pour gérer les objets non-dict (Chanson)
    class Config:
        orm_mode = True # ou from_attributes = True pour Python >= 3.11


class PlaylistModel(BaseModel):
    """Modèle pour la Playlist."""
    # L'id n'est pas un attribut de l'objet Playlist, mais il est retourné par l'insertion dans la BD
    # Dans la BD il y a id_playlist et nom dans la table PLAYLIST 
    id_playlist: Optional[int] 
    nom: str
    
    # La liste des chansons est un attribut de la Playlist 
    # Nous pourrions vouloir l'inclure dans la réponse
    # chansons: Optional[List[ChansonModel]] # Décommenter si vous voulez les chansons dans la réponse get

    class Config:
        orm_mode = True


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/joueur/", tags=["Joueurs"])
async def lister_tous_joueurs():
    """Lister tous les joueurs"""
    logging.info("Lister tous les joueurs")
    liste_joueurs = joueur_service.lister_tous()

    liste_model = []
    for joueur in liste_joueurs:
        liste_model.append(joueur)

    return liste_model


@app.get("/joueur/{id_joueur}", tags=["Joueurs"])
async def joueur_par_id(id_joueur: int):
    """Trouver un joueur à partir de son id"""
    logging.info("Trouver un joueur à partir de son id")
    return joueur_service.trouver_par_id(id_joueur)
    
# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
