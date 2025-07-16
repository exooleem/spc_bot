from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я живой и работаю на Render 🎉")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
