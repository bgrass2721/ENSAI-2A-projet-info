from business_object.playlist import Playlist
from business_object.chanson import Chanson

class PlaylistService:
    
    def add_chanson(self, playlist: Playlist, chanson: Chanson) -> bool:
        """
        Ajoute une chanson à une playlist.
        
        Args:
            playlist: L'objet Playlist
            chanson: L'objet Chanson à ajouter
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        if chanson not in playlist.chansons:
            playlist.chansons.append(chanson)
    
    def del_chanson(self, playlist: Playlist, chanson: Chanson) -> bool:
        """
        Supprime une chanson d'une playlist.
        
        Args:
            playlist: L'objet Playlist
            chanson: L'objet Chanson à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        if chanson in playlist.chansons:
            playlist.chansons.remove(chanson)