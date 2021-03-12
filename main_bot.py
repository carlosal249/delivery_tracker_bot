import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
)

import requests

endereco_entrega = 'rua marcos emilio verbinem, n150, Agua verde'

mensagem_endereco = print(f'Seu pedido foi aprovado, e sera entregue no endereco {endereco_entrega}.')

# Token provided by @ BotFather
TOKEN = '1604610917:AAGbRPaEPIQEf_tT2UE4ODkH6v8vBlvkOE0' 
# Your Heroku App Page 
APP_NAME = 'https://botdeliverytracker.herokuapp.com/'
# Port
PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
   '''
    Ola, Sou A penelope, bot da Drogaria Catarinense, e irei te enviar atualizacoes sobre seus pedidos \n 
    /start_tracking: para comecar a rastrear seus pedidos!
    '''
    )

# Location Tracking
LOC = range(1)

def start_tracking(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Driver: %s", user.first_name)
    update.message.reply_text(
        mensagem_endereco,
        reply_markup = ReplyKeyboardRemove(),
    )
    return LOC

def att_tracking(update: Update, context: CallbackContext):
    user = update.message.from_user
    last_location = update.message.location
    logger.info("Ola %s Sua encomenda saiu para entrega", user.first_name)

def cancel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Driver ID %s decided to cancel location record.", user.first_name, update.message.text)

    update.message.reply_text('Location record has been cancelled.')

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    '''Start Bot'''
    # Launch Updater
    updater = Updater("{}".format(TOKEN), use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # conversions handled by command
    dispatcher.add_handler(CommandHandler("start", start))

    # conversation handler
    loc_handler = ConversationHandler(
        entry_points = [CommandHandler('start_tracking', start_tracking)],
        states = {},
        fallbacks = [CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(loc_handler)

    # log all errors
    dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path="{}".format(TOKEN))
    
    updater.bot.set_webhook("{}".format(APP_NAME) + "{}".format(TOKEN))
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
