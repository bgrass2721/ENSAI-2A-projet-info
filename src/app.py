import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from client.chanson_client import ChansonClient
from client.playlist_client import PlaylistClient

#  Création et configuration de l’application FastAPI

app = FastAPI(title="API Mus’IA - Gestion des Playlists")
# initialiser_logs("Webservice Mus’IA")

playlist_client = PlaylistClient()
chanson_client = ChansonClient()

# Modèles Pydantic


class ParolesModel(BaseModel):
    """Modèle de représentation des paroles et du vecteur d'embedding."""

    vecteur: List[float]
    content: Optional[str] = None


class ChansonModel(BaseModel):
    """Modèle de représentation d’une chanson."""

    titre: str
    artiste: str
    paroles: Optional[ParolesModel]
    année: Optional[int]
    model_config = {"from_attributes": True}


class PlaylistModel(BaseModel):
    """Modèle de représentation d’une playlist."""

    id_playlist: Optional[int]
    nom: str
    chansons: Optional[List[ChansonModel]]

    model_config = {"from_attributes": True}


class PlaylistCreationModel(BaseModel):
    """Modèle d'entrée pour la création d'une playlist."""

    nom: str  # Mot-clé qui servira aussi de nom de playlist
    nbsongs: int  # Nombre de chansons souhaitées


class NewChansonInput(BaseModel):
    """
    Modèle Pydantic pour les données reçues lors d'une requête POST.
    Les paroles ne sont pas incluses car elles sont récupérées automatiquement.
    """

    titre: str
    artiste: str


class ParolesContentModel(BaseModel):
    """Modèle pour le retour des paroles simples."""

    titre: str
    artiste: str
    paroles: str


#   Redirection automatique vers la documentation interactive


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige l’utilisateur vers la page de documentation (Swagger UI)."""
    return RedirectResponse(url="/docs")


#   ENDPOINTS POUR LES PLAYLISTS


@app.post("/playlists", response_model=PlaylistModel, tags=["Playlists"])
async def create_playlist(data: PlaylistCreationModel):
    """
    Crée une playlist à partir d'un nom/mot-clé et d'un nombre de chansons.

    - Le nom fourni est utilisé comme mot-clé de recherche ET comme nom de playlist
    - Les chansons sont automatiquement recherchées basées sur le mot-clé
    - Retourne la playlist créée avec toutes ses chansons
    """
    try:
        # Validation des entrées
        if data.nbsongs <= 0 or data.nbsongs > 50:
            raise HTTPException(
                status_code=400, detail="Le nombre de chansons doit être entre 1 et 50"
            )

        if len(data.nom.strip()) < 2:
            raise HTTPException(
                status_code=400, detail="Le nom/mot-clé doit contenir au moins 2 caractères"
            )

        # Appel du client corrigé
        nouvelle_playlist_objet = playlist_client.request_playlist(
            keyword=data.nom,  # Utilise le nom comme mot-clé de recherche
            nbsongs=data.nbsongs,
        )

        if not nouvelle_playlist_objet:
            raise HTTPException(status_code=500, detail="La création de la playlist a échoué")

        # Conversion de l'objet Playlist métier en PlaylistModel
        chansons_model = []
        for chanson in nouvelle_playlist_objet.chansons:
            # Gestion des paroles (optionnelles)
            paroles_model = None
            if chanson.paroles:
                paroles_model = ParolesModel(
                    vecteur=chanson.paroles.vecteur, content=chanson.paroles.content
                )

            # Création du modèle de chanson
            chanson_model = ChansonModel(
                titre=chanson.titre,
                artiste=chanson.artiste,
                annee=chanson.annee,
                paroles=paroles_model,
            )
            chansons_model.append(chanson_model)

        # Création du modèle de playlist final
        playlist_model = PlaylistModel(
            id_playlist=getattr(nouvelle_playlist_objet, "id", None),
            nom=nouvelle_playlist_objet.nom,
            chansons=chansons_model,
        )

        return playlist_model

    except HTTPException:
        # Relance les exceptions HTTP déjà levées
        raise
    except Exception as e:
        logging.error(f"Erreur lors de la création de la playlist : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {e}")


@app.get("/playlists", response_model=List[PlaylistModel], tags=["Playlists"])
async def get_all_playlists():
    """
    Récupère la liste de toutes les playlists via le client.
    """
    try:
        playlists = playlist_client.get_playlists()
        return playlists
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des playlists via client : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.get("/playlists/{nom}", response_model=PlaylistModel, tags=["Playlists"])
async def get_playlist_by_nom(nom: str):
    """
    Récupère une playlist spécifique par son nom via le client.
    """
    try:
        playlist = playlist_client.get_playlist(nom)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist introuvable.")
        return playlist
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Erreur récupération playlist {nom} via client : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.get("/playlists/{nom}/songs", response_model=List[ChansonModel], tags=["Playlists"])
async def get_songs_from_playlist(nom: str):
    """
    Retourne toutes les chansons d'une playlist via le client.
    """
    try:
        chansons = playlist_client.get_playlist_chansons(nom)

        if chansons is None:
            raise HTTPException(status_code=404, detail="Playlist introuvable.")
        return chansons
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Erreur récupération chansons de playlist {nom} via client : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


#  ENDPOINTS POUR LES CHANSONS


@app.get(
    "/chansons/",
    response_model=List[ChansonModel],
    summary="Retourne la liste complète des chansons disponibles.",
)
async def get_all_chansons():
    """
    Récupère toutes les chansons via le client.
    """
    try:
        liste_chansons = chanson_client.get_chansons()
        return liste_chansons
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des chansons via client: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.post(
    "/chansons/",
    summary="Ajoute une chanson (récupération auto des paroles).",
)
async def add_chanson_from_api(chanson_data: NewChansonInput):
    """
    Création complète d'une chanson via le Client.
    """
    try:
        chanson_complete = chanson_client.add_new_chanson(
            titre=chanson_data.titre, artiste=chanson_data.artiste
        )
        return chanson_complete

    except Exception as e:
        logging.error(f"Échec de la création de la chanson via client: {e}")
        raise HTTPException(status_code=500, detail=f"Échec de la création de la chanson: {e}")


@app.get(
    "/chansons/search",  # NOUVEAU PATH
    response_model=ChansonModel,
    summary="Fournit les infos d'une chanson par titre et artiste.",
)
async def get_chanson_by_search(
    titre: str,
    artiste: str,  # NOUVEAUX PARAMETRES
):
    """
    Récupère une chanson spécifique par son titre et artiste via le client.
    """
    try:
        chanson = chanson_client.get_chanson_by_titre_artiste(
            titre, artiste
        )  # APPEL CLIENT MODIFIÉ

        if not chanson:
            raise HTTPException(
                status_code=404, detail=f"La chanson '{titre}' de {artiste} n'a pas été trouvée."
            )
        return chanson
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Erreur récupération chanson '{titre}' de {artiste} via client: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


@app.get(
    "/chansons/lyrics/search",  # NOUVEAU PATH
    response_model=ParolesContentModel,
    summary="Retourne le texte des paroles d'une chanson.",
)
async def get_lyrics_for_song(titre: str, artiste: str):  # NOUVEAUX PARAMETRES
    """
    Récupère le texte des paroles d'une chanson via le client.
    """
    try:
        paroles = chanson_client.get_lyrics_by_titre_artiste(titre, artiste)  # APPEL CLIENT MODIFIÉ

        if not paroles:
            raise HTTPException(
                status_code=404,
                detail=f"Le contenu des paroles n'est pas disponible pour '{titre}' de {artiste}.",
            )
        return paroles
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Erreur récupération paroles '{titre}' de {artiste} via client: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne.")


# --- Lancement de l'application ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
    logging.info("Arret du Webservice")
