Bot Readme
===================

This Python script implements a Telegram bot that provides currency conversion functionality, specifically tailored for a case by ТМК (TMK). The bot allows users to check the exchange rates of various currencies and calculate the price of commodities (iron and steel) in different currencies.

Setup Instructions
------------------

1.  **Clone the Repository:**
    
        git clone <repository-url>
        cd <repository-folder>
                    
    
2.  **Install Dependencies:**
    
    Ensure you have Python 3.x installed on your system. Then install the required dependencies using pip:
    
        pip install -r requirements.txt
                    
    
3.  **Setup Telegram Bot Token:**
    
    Obtain a token for your Telegram bot from the [BotFather](https://core.telegram.org/bots#6-botfather) and save it in a file named `.env` in the project directory:
    
        token=<your-telegram-bot-token>
                    
    
4.  **Run the Bot:**
    
    Execute the Python script `main.py` to start the bot:
    
        python main.py
                    
    

Bot Functionality
-----------------

*   **Currency Conversion:** Users can check the exchange rates of USD and CNY relative to RUB.
*   **Commodity Price Calculation:** Users can calculate the price of iron or steel in various currencies based on their weight.

Bot Commands
------------

*   **/start:** Initializes the bot and displays the default buttons for navigation.
*   **/help:** Provides information on how to use the bot.
*   **/about:** Displays information about the bot.

Usage
-----

1.  **Start the Bot:**
    
    Start a conversation with the bot on Telegram by searching for its username or clicking on the provided link.
    
2.  **Interact with the Bot:**
    *   Use the provided buttons to navigate through the available options.
    *   Alternatively, type commands or messages to interact with the bot.
3. **Commands:**

    * ### USD Exchange Rate🇺🇸
    
      Clicking this button will trigger the bot to retrieve and display the current exchange rate of the US Dollar (USD) relative to the Russian Ruble (RUB).
    
    * ### CNY Exchange Rate🇨🇳

      Clicking this button will prompt the bot to retrieve and show the current exchange rate of the Chinese Yuan (CNY) relative to the Russian Ruble (RUB).
    
    * ### Iron Ore Price⛏️
    
      Clicking this button will initiate a conversation with the bot to calculate the price of iron ore based on its weight. The bot will ask you to enter the weight         of iron ore in metric tons.
    
    * ### Steel Price👷
    
      Clicking this button will start a conversation with the bot to calculate the price of steel based on its weight. The bot will ask you to enter the weight of            steel in metric tons.
    
    * ### Back to Start🏠
    
      Clicking this button will return you to the initial menu where you can access other options and commands provided by the bot.
    
    * ### About the Bot🤖
    
      Clicking this button will display information about the bot, providing details about its purpose and functionality.


Contributors
------------

*   [Gleb Timoshenko](https://github.com/GTimoshenko) - Developer
*   [Daniil Kozlov](https://github.com/SenyaPevko) - Developer
