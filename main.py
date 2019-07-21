from updater import dispatcher, updater
from handlers import app_conv_handler, start_handler
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(app_conv_handler)

updater.start_polling()