import lyricsgenius
from settings import GENIUS_TOKEN

# Performs a search with the lyricsgenius module
def get_lyrics_genius(song, artist):
    genius = lyricsgenius.Genius(GENIUS_TOKEN)
    song = genius.search_song(song, artist)
    if song is None:
        return None
    return song.lyrics