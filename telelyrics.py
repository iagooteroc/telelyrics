# -*- coding: utf-8 -*-
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
							ConversationHandler, PicklePersistence)
from lyrics import get_lyrics_genius
import logging
import os
import json
import time
import auth
import spotipy
from lyrics import get_lyrics_genius
from settings import BOT_TOKEN
TYPING_URL = 1

# Scope of Spotify token access
scope = 'user-read-currently-playing'

# Name of logfile
LOG_FILENAME = 'telelyrics.log'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=LOG_FILENAME)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20000000, backupCount=3)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Returns currently playing track data using spotipy
def get_currently_playing(token):
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_playing_track()

""" 
Answers to /lyrics command.
Checks if there is an auth token in cache and if there is none, asks for it
If there is, gets the currently playing song using spotipy
and the lyrics using lyricsgenius.
"""
def lyrics(bot, update, user_data):
    user_id = str(update.message.chat_id) + '_' + update.message.from_user['username']
    logging.info("Starting lyrics for user_id: {}".format(user_id))
    sp_oauth = auth.get_auth(username=user_id, scope=scope)
    token_info = sp_oauth.get_cached_token()
    # If there is no cached token, ask for it
    if not token_info:
        reply_text = "Token unavaliable. Please visit {} and paste/share the url you obtain (https://localhost...).".format(sp_oauth.get_authorize_url())
        update.message.reply_text(reply_text)
        user_data['sp_oauth'] = sp_oauth
        logging.info("text: %s, reply: %s", update.message.text, reply_text)
        return TYPING_URL
    else:
        token = token_info['access_token']
        current = get_currently_playing(token)
        if not current:
            reply_text = "No song currently playing."
            update.message.reply_text(reply_text)
            logging.info("text: %s, reply: %s", update.message.text, reply_text)
            return ConversationHandler.END
        item = current['item']
        if not item:
            reply_text = "No song detected. Perhaps it's a podcast?"
            update.message.reply_text(reply_text)
            logging.info("text: %s, reply: %s", update.message.text, reply_text)
            return ConversationHandler.END
        name = item['name']
        artist = item['artists'][0]['name']
        l = get_lyrics_genius(song=name, artist=artist)
        if l:
            reply_text = "Song: {}\nArtist: {}\n{}".format(name, artist, l)
        else:
            reply_text = "Sorry, no lyrics found for song: {}, artist: {}".format(name, artist)
        update.message.reply_text(reply_text)
        logging.info("text: %s, reply: %s", update.message.text, reply_text)
        return ConversationHandler.END

"""
Receives authentication url and checks its validity.
If it's valid, it caches it.
"""
def received_url(bot, update, user_data):
    sp_oauth = user_data['sp_oauth']
    code = sp_oauth.parse_response_code(update.message.text)
    if not code:
        reply_text = "Oops! Something went wrong. Make sure to copy all the url, including the https://localhost..."
        update.message.reply_text(reply_text)
        logging.info("text: %s, reply: %s", update.message.text, reply_text)
        return ConversationHandler.END
    token_info = sp_oauth.get_access_token(code)
    print(token_info['access_token'])
    reply_text = "Great! Access token saved in cache."
    update.message.reply_text(reply_text)
    logging.info("text: %s, reply: %s", update.message.text, reply_text)
    return ConversationHandler.END

# Log Errors caused by Updates
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# Starts the bot
def main():
    #  Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='telelyricsbot')
    updater = Updater(BOT_TOKEN, persistence=pp)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('lyrics', lyrics, pass_user_data=True)],
        states={
            TYPING_URL: [MessageHandler(Filters.text,
                                          received_url,
                                          pass_user_data=True)]
        },
        fallbacks=[],
        name="conversation",
        allow_reentry=True,
        persistent=True
    )
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()