from telegram.ext import CommandHandler
from updater import dispatcher, updater
from views.welcome import welcome
from  views.authentication import auth_handler
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

start_handler = CommandHandler('start', welcome)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(auth_handler)

updater.start_polling()
