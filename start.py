from client.chanson_client import ChansonClient
# from client.playlist_client import PlaylistClient
from dao.dao import DAO

DAO()._drop_table()
DAO()

musiques = [
["Bohemian Rhapsody","Queen"],
["Billie Jean","Michael Jackson"],
["Smells Like Teen Spirit","Nirvana"],
["Imagine","John Lennon"],
["Hotel California","Eagles"],
["Shape of You","Ed Sheeran"],
["Rolling in the Deep","Adele"],
["Thriller","Michael Jackson"],
["Hey Jude","The Beatles"],
["Let It Be","The Beatles"],
["Staying Alive","Bee Gees"],
["Like a Rolling Stone","Bob Dylan"],
["Sweet Child O' Mine","Guns N' Roses"],
["Wonderwall","Oasis"],
["Lose Yourself","Eminem"],
["Hallelujah","Leonard Cohen"],
["All of Me","John Legend"],
["Take On Me","a-ha"],
["Africa","Toto"],
["Beat It","Michael Jackson"],
["Uptown Funk","Mark Ronson ft. Bruno Mars"],
["Bad Guy","Billie Eilish"],
["Blinding Lights","The Weeknd"],
["Someone Like You","Adele"],
["Poker Face","Lady Gaga"],
["Born This Way","Lady Gaga"],
["Viva la Vida","Coldplay"],
["Fix You","Coldplay"],
["Clocks","Coldplay"],
["Back in Black","AC/DC"],
["Highway to Hell","AC/DC"],
]

i=0
for musique in musiques:
    ChansonClient().add_new_chanson(musique[0], musique[1])
    i=i+1
    print(i)

# chansons = ChansonClient().get_chansons()

# for chanson in chansons:
#     print(chanson.afficher())

# playlist_1 = PlaylistClient().request_playlist("amour", 5)

# playlists = PlaylistClient().get_playlists()

# for playlist in playlists:
#     print(playlist.afficher())
