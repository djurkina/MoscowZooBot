import smtplib
from email.mime.text import MIMEText
from telegram import Update
from telegram.ext import ContextTypes


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_message = update.message.text
    try:
        msg = MIMEText(f"Обратная связь от пользователя {user_name} ({user_id}):\n\n{user_message}")
        msg['Subject'] = 'Обратная связь с бота'
        msg['From'] = 'ndjurkina@gmail.com'
        msg['To'] = 'user8087@gmail.com'
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('yndjurkina@gmail.com', 'vEtEr2323')
            smtp.send_message(msg)
            await update.message.reply_text("Ваше сообщение отправлено. Спасибо!")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при отправке сообщения: {e}")
