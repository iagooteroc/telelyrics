# Telelyrics - Gets the lyrics of the song you're playing in Spotify
Telegram bot written in python using [the python-telegram-bot library](https://github.com/python-telegram-bot/python-telegram-bot). It uses [spotipy, a lightweight Python library for the Spotify Web API](https://github.com/plamere/spotipy), to obtain the currently playing song in your account and performs a search in [the Genius API](http://genius.com/api-clients), with [the lyricsgenius pachage](https://github.com/johnwmillr/LyricsGenius/blob/master/README.md), to get the lyrics.

## Setup
You will need a (free) account that authorizes access to [the Genius API](http://genius.com/api-clients). More info on [the lyricsgenius github.](https://github.com/johnwmillr/LyricsGenius#setup)
You will also need a Telegram Bot token and Spotify API credentials. 
You can get your credentials at https://developer.spotify.com/my-applications and set them by setting environment variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```
To set the other credentials simply fill the settings.py file like this:
```
GENIUS_TOKEN = 'your-genius-token'
BOT_TOKEN = "your-bot-token"
```

## Dependencies
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and [lyricsgenius](https://github.com/johnwmillr/LyricsGenius/) can be installed by running:
```
pip3 install -r requirements.txt
```
### But
For some reason, the spotipy pip package is not up to date so it has to be installed directly from github like:
```
pip3 install -e git+https://github.com/plamere/spotipy.git#egg=hyde
```
