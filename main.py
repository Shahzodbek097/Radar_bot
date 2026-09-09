from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler  # inline buttonlar uchun
from handlers import start_handler, massage_handler
from config import *


def main():
    updater=Updater(TOKEN)
    dispatcher=updater.dispatcher
    dispatcher.add_handler(CommandHandler("start",start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, massage_handler))
    # dispatcher.add_handler(CallbackQueryHandler(massage_handler))   # inline button uchun ishlatiladi
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()

