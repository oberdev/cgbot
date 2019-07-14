from telegram.ext import Updater
from dotenv import load_dotenv
import os

load_dotenv()

updater: Updater = Updater(
    token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher
