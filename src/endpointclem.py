import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# -------------------------------------------------------------------
#  Import des DAO spécialisés (accès aux tables de la base PostgreSQL)
# -------------------------------------------------------------------
from dao.dao_playlist import DAO_playlist     # Gestion des playlists
from dao.dao_chanson import DAO_chanson       # Gestion des chansons
from dao.dao_paroles import DAO_paroles       # Gestion des paroles

# -------------------------------------------------------------------
#  Import des classes métiers (Business Layer)
# -------------------------------------------------------------------
from business_object.playlist import Playlist
from business_object.chanson import Chanson
from business_object.paroles import Paroles

# -------------------------------------------------------------------
#  Import de l'outil d'initialisation des logs
# -------------------------------------------------------------------
from utils.log_init import initialiser_logs


# -------------------------------------------------------------------
#  Création et configuration de l’application FastAPI
# -------------------------------------------------------------------
app = FastAPI(title="API Mus’IA - Gestion des Playlists")
initialiser_logs("Webservice Mus’IA")

# On crée des instances de DAO pour communiquer avec la base
dao_playlist = DAO_playlist()
dao_chanson = DAO_chanson()
dao_paroles = DAO_paroles()


# -------------------------------------------------------------------
#  Définition des modèles Pydantic
# Ces modèles servent à valider et formater les données échangées
# entre le client (requêtes HTTP) et le serveur (API)
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
        orm_mode = True  # Autorise la conversion automatique d’un objet Python en JSON


class PlaylistModel(BaseModel):
    """Modèle de représentation d’une playlist."""
    id_playlist: Optional[int]
    nom: str
    chansons: Optional[List[ChansonModel]]

    class Config:
        orm_mode = True


class PlaylistCreationModel(BaseModel):
    """Modèle d'entrée pour la création d'une playlist."""
    nom: str        # Nom choisi par l’utilisateur
    keyword: str    # Mot-clé représentant l’ambiance ou le thème
    nbsongs: int    # Nombre de chansons souhaitées dans la playlist


# -------------------------------------------------------------------
#  Redirection automatique vers la documentation interactive
# -------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redirige l’utilisateur vers la page de documentation interactive de l’API.
    (Swagger UI : /docs)
    """
    return RedirectResponse(url="/docs")


# ===================================================================
#  SECTION : ENDPOINTS POUR LES PLAYLISTS
# ===================================================================

@app.post("/playlists", response_model=PlaylistModel, tags=["Playlists"])
async def create_playlist(data: PlaylistCreationModel):
    """
    Crée une playlist à partir d’un mot-clé et d’un nombre de chansons souhaité.
    Les chansons sont pour l’instant générées automatiquement à partir du mot-clé.
    """
    try:
        # ---  Génération temporaire de chansons (pour la démo)
        chansons = []
        for i in range(data.nbsongs):
            titre = f"{data.keyword.capitalize()} Song {i+1}"
            artiste = f"Artiste {i+1}"
            annee = 2020 + i
            # On crée un objet Paroles (vecteur factice pour le moment)
            paroles = Paroles(content=f"Paroles {data.keyword} {i+1}", vecteur=[float(i)])
            # Création de l’objet Chanson
            chanson = Chanson(titre, artiste, annee, paroles)
            # Ajout de la chanson dans la base de données
            dao_chanson.add_chanson(chanson)
            chansons.append(chanson)

        # ---  Création de la playlist contenant ces chansons
        playlist = Playlist(data.nom, chansons)
        dao_playlist.add_playlist(playlist)

        # ---  Retourne la playlist créée (sous format JSON)
        return PlaylistModel(
            nom=playlist.nom,
            chansons=[
                ChansonModel(
                    titre=c.titre,
                    artiste=c.artiste,
                    annee=c.annee,
                    paroles=ParolesModel(vecteur=c.paroles.vecteur, content=c.paroles.content)
                ) for c in chansons
            ]
        )

    except Exception as e:
        logging.error(f"Erreur lors de la création de la playlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la playlist.")


@app.get("/playlists", response_model=List[PlaylistModel], tags=["Playlists"])
async def get_all_playlists():
    """
    Récupère et retourne la liste de toutes les playlists enregistrées dans la base.
    """
    try:
        playlists = dao_playlist.get_playlists()
        result = []
        for p in playlists:
            chansons = [
                ChansonModel(
                    titre=c.titre,
                    artiste=c.artiste,
                    annee=c.annee,
                    paroles=ParolesModel(vecteur=c.paroles.vecteur, content=c.paroles.content)
                )
                for c in p.chansons
            ]
            result.append(PlaylistModel(nom=p.nom, chansons=chansons))
        return result

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des playlists : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des playlists.")


@app.get("/playlists/{id_playlist}", response_model=PlaylistModel, tags=["Playlists"])
async def get_playlist_by_id(id_playlist: int):
    """
    Récupère une playlist spécifique à partir de son identifiant unique.
    """
    playlist = dao_playlist.get_playlist_from_id(id_playlist)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist introuvable.")

    chansons = [
        ChansonModel(
            titre=c.titre,
            artiste=c.artiste,
            annee=c.annee,
            paroles=ParolesModel(vecteur=c.paroles.vecteur, content=c.paroles.content)
        )
        for c in playlist.chansons
    ]
    return PlaylistModel(nom=playlist.nom, chansons=chansons)


@app.get("/playlists/{id_playlist}/songs", response_model=List[ChansonModel], tags=["Playlists"])
async def get_songs_from_playlist(id_playlist: int):
    """
    Retourne toutes les chansons associées à une playlist donnée.
    """
    playlist = dao_playlist.get_playlist_from_id(id_playlist)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist introuvable.")

    chansons = [
        ChansonModel(
            titre=c.titre,
            artiste=c.artiste,
            annee=c.annee,
            paroles=ParolesModel(vecteur=c.paroles.vecteur, content=c.paroles.content)
        )
        for c in playlist.chansons
    ]
    return chansons
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
        liste_chansons_bo = dao_chanson.get_chansons() 
    except Exception as e:
        # Gère les erreurs de connexion/exécution de la base de données
        print(f"Erreur DAO lors de la récupération des chansons: {e}")
        raise HTTPException(status_code=500, detail="Une erreur interne est survenue lors de la récupération des chansons.")

    # Conversion des Business Objects en Pydantic Models
    liste_model = [convert_chanson_to_model(chanson) for chanson in liste_chansons_bo]

    return liste_model

# --- Endpoint pour l'ajour d'une chanson ---

class NewChansonInput(BaseModel):
    """Modèle Pydantic pour les données reçues lors d'une requête POST."""
    titre: str
    artiste: str
    annee: Optional[int] = None # L'année est facultative (default None dans Chanson)
    paroles: str

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

# --- Endpoint pour la Consultation d’une Chanson Spécifique ---

@app.get("/chansons/{chanson_id}", 
         response_model=ChansonModel, 
         summary="Fournit les infos d'une chanson par son ID.")
async def get_chanson_by_id(
    chanson_id: int = Path(..., title="L'ID de la chanson à récupérer", ge=1)
):
    """
    Récupère une chanson spécifique en utilisant son identifiant entier (ID)
    stocké dans la base de données.
    """

    chanson_bo = dao.get_chanson_from_id(chanson_id)
    
    if not chanson_bo:
        raise HTTPException(
            status_code=404, 
            detail=f"La chanson avec l'ID {chanson_id} n'a pas été trouvée."
        )
    return convert_chanson_to_model(chanson_bo)
# --- Endpoint pour la Consultation des Paroles---

class ParolesContentModel(BaseModel):
    titre: str
    artiste: str
    paroles: str

@app.get("/chansons/{chanson_id}/lyrics", 
         response_model=ParolesContentModel, 
         summary="Retourne le texte des paroles stockées d'une chanson.")
async def get_lyrics_for_song(
    chanson_id: int = Path(..., title="L'ID de la chanson", ge=1)
):
    """
    Récupère le texte (content) des paroles d'une chanson 
    directement depuis la base de données.
    """
    chanson_bo = dao.get_chanson_from_id(chanson_id)
    
    if not chanson_bo:
        raise HTTPException(
            status_code=404, 
            detail=f"La chanson avec l'ID {chanson_id} n'a pas été trouvée."
        )
    if not chanson_bo.paroles or not chanson_bo.paroles.content:
        raise HTTPException(
            status_code=404, 
            detail=f"Le contenu des paroles n'est pas disponible pour la chanson ID {chanson_id}."
        )
    return ParolesContentModel(
        titre=chanson_bo.titre,
        artiste=chanson_bo.artiste,
        paroles=chanson_bo.paroles.content
    )

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
