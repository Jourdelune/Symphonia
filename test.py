import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="bc1f01e2722747699311b953fb45e8df",
                                                           client_secret="9a2fa3f8100744d7a984bf67a256b5ad"))

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])