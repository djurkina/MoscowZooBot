from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from my_bot.quiz import handle_quiz
from my_bot.opeca import handle_opeca_callback
from animals import animals

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Программа опеки", callback_data="show_animals")],
        [InlineKeyboardButton("Начать викторину", callback_data="start_quiz")]
    ])
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=keyboard)

async def handle_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "start_quiz":
        await handle_quiz(update, context)
    if query.data == "show_animals":
        await show_animals_callback(update, context)

async def show_animals_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(animal, callback_data=f"show_animal_{animal}")] for animal in animals
        ]
    )
    await update.callback_query.message.reply_text("Выберите животное:", reply_markup=keyboard)

async def handle_animal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    animal_name = query.data.replace("show_animal_", "")
    await query.answer()
    await handle_opeca_callback(update, context, animal_name)
