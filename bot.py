import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ===== НАСТРОЙКИ =====
OPENAI_API_KEY = "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"
TELEGRAM_TOKEN = "8285599492:AAE6YguLaWTZfTu6O46D4q3rSKnjTyIDKxw"

openai.api_key = OPENAI_API_KEY

# ===== ЛОГИ =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== КОМАНДЫ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name if update.effective_user else "друг"
    await update.message.reply_text(
        f"Привет, {user}! 👋\n"
        f"Я твой фриланс-помощник на базе GPT 🤖\n\n"
        f"Напиши сообщение — и я помогу тебе с ответом, текстом, идеей или чем угодно!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Доступные команды:\n"
        "/start — перезапустить бота\n"
        "/help — список команд\n\n"
        "Просто отправь любое сообщение, и я отвечу с помощью GPT ✨"
    )

# ===== ОСНОВНАЯ ЛОГИКА GPT =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    user = update.effective_user.first_name if update.effective_user else "Пользователь"
    logger.info(f"{user} написал: {user_text}")

    if not user_text:
        await update.message.reply_text("⚠️ Пустое сообщение, попробуй еще раз.")
        return

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Ответь профессионально и дружелюбно на сообщение: {user_text}",
            max_tokens=300,
            temperature=0.8,
        )
        answer = response.choices[0].text.strip()
        await update.message.reply_text(answer or "🤔 Не могу придумать ответ.")
    except Exception as e:
        logger.error(f"Ошибка GPT: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке запроса. Попробуй позже.")

# ===== ЗАПУСК =====
def main():
    logger.info("🚀 Запуск бота...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Бот успешно запущен и слушает сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
