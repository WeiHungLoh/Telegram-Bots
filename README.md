# Telegram Bots

This repository contains Python scripts for multiple Telegram bots with different functionalities, including a To-Do List bot, Weather bot, and User Info bot.
Each bot has specific features and can be set up independently. When accessing 

You may interact with the original bots here:
- [To-Do List Bot](https://t.me/ToDoListxBot)
- [Weather Bot](https://t.me/Weathersgxbot)
- [User Info Bot](https://t.me/userinformationxbot)

*Note: These bots will only be functional when the corresponding Python script is running locally on my laptop (it is not running on cloud)*

### General Setup
Before starting, ensure you have the following installed:
- Python 3.12.2
- Pip3 (python package installer)
  
### Installation
Open your terminal and go to the directory you want to clone into.
1. Clone the repositories:
   ```bash
   cd path/to/your/directory
   git clone https://github.com/WeiHungLoh/Telegram-Bots
   ```

3. Install the dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
### Creating a Telegram Bot and Retrieving Token
1. Click [here](https://t.me/BotFather)
2. Use the command "/newbot" to create a new bot. Follow the instructions to choose a name and username for the bot
3. Save the bot token generated

### Retrieving OpenWeatherMap API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/)
2. Create a new account if you don't have one, then click on "My API keys" under your username dropdown
3. Save the API key generated

### Configuration
Before running these bots, you have to "replace bot_token" and "api_key" with your actual token and API keys.

### Note
When accessing the hyperlinks above, right-click on the link and select "Open in a new tab" to avoid disruptions.
