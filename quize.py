from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from questions import questions

async def handle_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data['answers'] = {}
    user_data['current_question'] = 0
    try:
        await ask_question(update, context)
    except Exception as e:
        await update.message.reply_text(f"Произошла неизвестная ошибка: {e}")

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    question_index = user_data['current_question']
    if question_index < len(questions):
        q = questions[question_index]
        keyboard = ReplyKeyboardMarkup([[option] for option in q["options"]], resize_keyboard=True)
        await update.message.reply_text(q["question"], reply_markup=keyboard)
    else:
        await show_results(update, context)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_answer = update.message.text
    question_index = user_data['current_question']
    try:
        q = questions[question_index]
        if user_answer in q["options"]:
            user_data['answers'][q["question"]] = user_answer
            user_data['current_question'] += 1
            await ask_question(update, context)
        else:
            await update.message.reply_text("Пожалуйста, выберите один из предложенных вариантов.")
    except IndexError:
        await update.message.reply_text("Ошибка в обработке ответа. Попробуйте начать викторину заново.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")


async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    answers = user_data['answers']
    animal_scores = {}
    for q in questions:
        if q["question"] in answers:
            selected_answer = answers[q["question"]]
            for animal, score_points in q['scores'].items():
                if selected_answer == animal:
                    animal_scores[score_points] = animal_scores.get(score_points, 0) + 1
    if animal_scores:
        winning_animal = max(animal_scores, key=animal_scores.get)
        try:
           await update.message.reply_text(f"Ваше тотемное животное: {winning_animal.title()}!")
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")
    else:
        await update.message.reply_text("Не удалось определить ваше тотемное животное.")
