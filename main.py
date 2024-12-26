import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import TOKEN
from quiz import handle_quiz, handle_answer
from opeca import handle_opeca_callback
from handlers import start, handle_start_callback, show_animals_callback, handle_animal_callback
from feedback import feedback

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", handle_quiz))
    application.add_handler(CommandHandler("feedback", feedback))


    application.add_handler(CallbackQueryHandler(handle_start_callback, pattern="^(start_quiz|show_animals)$"))
    application.add_handler(CallbackQueryHandler(handle_animal_callback, pattern="^(show_animal_)"))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    application.run_polling()


if __name__ == '__main__':
    main()
