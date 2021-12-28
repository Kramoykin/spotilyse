import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os.path import expanduser
import time
from tools.getters import get_releases
from tools.getters import get_albums_tracks
from tools.utils import write_yaml
from tools.utils import read_yaml



# initialize spotify client with client credentials
# (client credentials should be set as environmental variables on your OS)
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

df_rel = get_releases(spotify, 
                      country = 'US', 
                      path = expanduser('~') + '/Projects/spotilyse/data/releases/albums/')
albums = df_rel['id'].tolist()

write_yaml(
    df_rel,
    'id',
    'releases_id_RU',
    path = expanduser('~') + '/Projects/spotilyse/config/'
    )

albums_ids = read_yaml(
    expanduser('~') + '/Projects/spotilyse/config/releases_id_RU.yaml',
    key = 'id')
print(albums_ids)

print(df_rel)

start_time = time.time()
df_tracks = get_albums_tracks(spotify,
                              country = 'US',
                              albums_ids = albums,
                              path = expanduser('~') + '/Projects/spotilyse/data/releases/tracks/')
print("--- %s seconds ---" % (time.time() - start_time))