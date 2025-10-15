import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import os

# ====== НАСТРОЙКИ (читаем из переменных окружения на Render) ======
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = OPENAI_API_KEY

# ====== ЛОГИ ======
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== КОМАНДЫ ======
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот на базе GPT. Отправь мне сообщение, и я отвечу :)")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Просто напиши любое сообщение, и я дам ответ. Команда /start — чтобы начать.")

# ====== ОБРАБОТКА СООБЩЕНИЙ ======
def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    logger.info(f"Пользователь написал: {user_text}")

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_text,
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        update.message.reply_text(answer)
    except Exception as e:
        logger.error(f"Ошибка GPT: {e}")
        update.message.reply_text("Произошла ошибка при обработке запроса. Попробуй позже.")

# ====== ОСНОВНОЙ ЦИКЛ ======
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    logger.info("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
