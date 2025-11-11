from client.chanson_client import ChansonClient
from client.playlist_client import PlaylistClient
from dao.dao import DAO

DAO()._drop_table()
DAO()

ChansonClient().add_new_chanson("Imagine", "John Lennon")
ChansonClient().add_new_chanson("Hey Jude", "The Beatles")
ChansonClient().add_new_chanson("Let It Be", "The Beatles")

chansons = ChansonClient().get_chansons()

for chanson in chansons:
    print(chanson.afficher())

playlist_1 = PlaylistClient().request_playlist("amour", 5)

playlists = PlaylistClient().get_playlists()

for playlist in playlists:
    print(playlist.afficher())