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

# -------------------------------------------------------------------
#  Lancement du serveur (pour exécution directe du script)
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # Le serveur démarre en local sur le port 9876
    uvicorn.run(app, host="0.0.0.0", port=9876)
