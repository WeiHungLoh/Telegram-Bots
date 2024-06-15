from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

api_key = "REPLACE_WITH_YOUR_API_KEY"
bot_token = "REPLACE_WITH_YOUR_TELEGRAM_BOT_TOKEN"

# List down the cities available
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the Weather Bot! \n\nPlease type /weather <city> to get the weather information \n\nPlease click this link: https://openweathermap.org/storage/app/media/cities_list.xlsx to check the list of cities")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_input = ' '.join(context.args)
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}"
        )

        if weather_data.json()['cod'] == '404':
            await update.message.reply_text("No city found")
        
        # Retrieves weather information from the API
        weather = weather_data.json()['weather'][0]['main']
        temp = weather_data.json()['main']['temp']
        # Convert from Kelvin to Celsius
        celsius = round(temp - 273.15, 1)
        wind = weather_data.json()['wind']['speed']
        humidity = weather_data.json()['main']['humidity']

        await update.message.reply_text(
            f"The weather in {user_input} is: {weather}\n"
            f"The temperature in {user_input} is: {celsius} degree Celsius\n"
            f"The wind speed in {user_input} is: {wind} km/h\n"
            f"The humidity in {user_input} is: {humidity}%"
        )        
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again.")

async def handletext(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I didn't recognise that command. Please type /start to check the available commands")

def main() -> None:
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(MessageHandler(~filters.COMMAND, handletext))


    application.run_polling()

if __name__ == '__main__':
    main()
