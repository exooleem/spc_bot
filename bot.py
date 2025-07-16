from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import os

# Получение токена и ID админа из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Этапы анкеты
NAME, CITY, WHY = range(3)

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Добро пожаловать в Successful People Club, {update.effective_user.first_name}.\n"
        "Чтобы оставить заявку, напиши /apply.\n"
        "Отменить — /cancel."
    )

# Команда /apply
async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Из какого ты города?")
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    await update.message.reply_text("Почему ты хочешь вступить в клуб?")
    return WHY

async def get_why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['why'] = update.message.text
    user = context.user_data

    # Текст для админа
    text = (
        "📩 Новая заявка на вступление в клуб:\n"
        f"👤 Имя: {user['name']}\n"
        f"🏙️ Город: {user['city']}\n"
        f"💬 Почему: {user['why']}\n"
        f"Telegram: @{update.effective_user.username or 'нет username'}"
    )

    # Ответ пользователю и отправка админу
    await update.message.reply_text("Спасибо! Мы свяжемся с тобой после рассмотрения заявки.")
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка отменена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("apply", apply)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            WHY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_why)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    app.run_polling()

if __name__ == '__main__':
    main()
