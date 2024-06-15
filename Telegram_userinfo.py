from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

bot_token = "REPLACE_WITH_YOUR_TELEGRAM_BOT_TOKEN"

async def handletext(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I didn't recognise that command. Please type /start to retrieve your Telegram details")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    username = user.username
    user_id = user.id
    language = user.language_code
    telegram_name = user.first_name
    print(f"Telegram Name: {telegram_name} \nUsername: {username} \nLanguage: {language} \nTelegram User ID: {user_id}")
    await update.message.reply_text(f"Telegram Name: {telegram_name} \nUsername: {username} \nLanguage: {language} \nTelegram User ID: {user_id}")

def main() -> None:
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(~filters.COMMAND, handletext))
    
    application.run_polling()

if __name__ == '__main__':
    main()