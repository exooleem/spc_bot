import os
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

NAME, CITY, WHY = range(3)

async def старт(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Добро пожаловать в Successful People Club, {update.effective_user.first_name}.\n"
        "Чтобы подать заявку, напишите /заявка.\n"
        "Отменить — /отмена."
    )

async def заявка(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как вас зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Из какого вы города?")
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Почему вы хотите вступить в клуб?")
    return WHY

async def get_why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["why"] = update.message.text
    user = context.user_data

    tg_user = update.effective_user
    if tg_user.username:
        user_link = f"@{tg_user.username}"
    else:
        user_link = f"[без username](tg://user?id={tg_user.id})"

    text = (
        "📩 Новая заявка на вступление в клуб:\n"
        f"👤 Имя: {user['name']}\n"
        f"🏙️ Город: {user['city']}\n"
        f"💬 Почему: {user['why']}\n"
        f"Telegram: {user_link}"
    )

    await update.message.reply_text(
        "Спасибо! Мы свяжемся с вами после рассмотрения заявки.",
        reply_markup=ReplyKeyboardRemove()
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка отменена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("заявка", заявка)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            WHY:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_why)],
        },
        fallbacks=[CommandHandler("отмена", cancel)],
    )

    app.add_handler(CommandHandler("старт", старт))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
