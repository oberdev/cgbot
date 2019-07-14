from telegram.ext import CommandHandler
from dotenv import load_dotenv
from updater import dispatcher, updater
from views.welcome import welcome
import logging
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

start_handler = CommandHandler('start', welcome)
dispatcher.add_handler(start_handler)

updater.start_polling()
