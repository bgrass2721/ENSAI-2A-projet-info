@app.post("/playlists", response_model=PlaylistModel, tags=["Playlists"])
async def create_playlist(data: PlaylistCreationModel):
    """
    Crée une playlist automatiquement à partir d’un mot-clé (thème ou genre musical)
    et du nombre de chansons souhaité.
    """
    logging.info(f"Création d'une playlist : {data.nom}, mot-clé = {data.keyword}")

    try:
        playlist = dao.creer_playlist_auto(data.nom, data.keyword, data.nbsongs)
        return PlaylistModel(id_playlist=playlist.id_playlist, nom=playlist.nom)
    except Exception as e:
        logging.error(f"Erreur lors de la création de la playlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la playlist.")


@app.get("/playlists", response_model=List[PlaylistModel], tags=["Playlists"])
async def get_all_playlists():
    """
    Retourne la liste complète des playlists stockées dans la base.
    """
    logging.info("Récupération de toutes les playlists.")
    try:
        playlists = dao.recuperer_playlists()
        return [PlaylistModel(id_playlist=p.id_playlist, nom=p.nom) for p in playlists]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des playlists : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des playlists.")


@app.get("/playlists/{id_playlist}", response_model=PlaylistModel, tags=["Playlists"])
async def get_playlist_by_id(id_playlist: int):
    """
    Retourne toutes les informations d’une playlist donnée à partir de son identifiant.
    """
    logging.info(f"Récupération de la playlist {id_playlist}.")
    playlist = dao.recuperer_playlist_par_id(id_playlist)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist introuvable.")
    return PlaylistModel(id_playlist=playlist.id_playlist, nom=playlist.nom)


@app.get("/playlists/{id_playlist}/songs", response_model=List[ChansonModel], tags=["Playlists"])
async def get_songs_from_playlist(id_playlist: int):
    """
    Fournit l’ensemble des chansons associées à une playlist donnée.
    """
    logging.info(f"Récupération des chansons de la playlist {id_playlist}.")
    chansons = dao.recuperer_chansons_par_playlist(id_playlist)
    if not chansons:
        raise HTTPException(status_code=404, detail="Aucune chanson trouvée pour cette playlist.")
    return [ChansonModel(id=c.id, titre=c.titre, artiste=c.artiste, annee=c.annee) for c in chansons]