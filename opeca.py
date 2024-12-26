from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from animals import animals
from pathlib import Path


async def handle_opeca_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, animal_name: str = None):
    if not animal_name:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(animal, callback_data=f"show_animal_{animal}")] for animal in animals
        ])
        await update.callback_query.message.reply_text("Выберите животное:", reply_markup=keyboard)
        return
    try:
       animal = animals.get(animal_name)
       if animal:
          photo_path = Path(animal.get("photo"))
          if not photo_path.exists():
               await update.callback_query.message.reply_text(f"Файл изображения не найден: {animal.get('photo')}")
               return
          with open(photo_path, 'rb') as photo:
              text = f"{animal_name.title()}:\n{animal.get('description')}\n\n"
              if "care_programs" in animal:
                 text += "Вы можете внести свой вклад:\n"
                 for program in animal["care_programs"]:
                     text += f"  - {program}\n"
              await update.callback_query.message.reply_photo(
                  caption=text,
                  photo=photo
              )
    except FileNotFoundError:
        await update.callback_query.message.reply_text(f"Файл изображения не найден: {animal.get('photo')}")
    except Exception as e:
        await update.callback_query.message.reply_text(f"Произошла ошибка: {e}")
