import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("BOT_TOKEN")

# Check if the token is set
if TOKEN is None:
    logging.error("Bot token not found. Please set the BOT_TOKEN environment variable.")
    exit(1)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=TOKEN)

# Initialize dispatcher
dp = Dispatcher()

@dp.message()
async def start_cmd(message: types.Message):
    # Send a welcome message when users start interacting with the bot
    await message.answer("""
👋 Hello and welcome to the Bitcoin Monitor Bot! 🚀

I'm here to keep you updated on the latest Bitcoin prices and provide valuable insights into the cryptocurrency market. Whether you're a seasoned investor or just curious about Bitcoin, I've got you covered!

📈 **Current Bitcoin Price:**
Just type /price to get the most recent Bitcoin price.

📊 **Market Insights:**
Use /stats to access detailed market statistics and trends.

📅 **Historical Data:**
For historical data, simply type /history followed by the desired time frame.

🔔 **Price Alerts:**
Set up price alerts with /setalert to receive notifications when Bitcoin hits your specified threshold.

Feel free to explore the various commands, and don't hesitate to ask if you have any questions. Happy monitoring! 🌐💰
    """)

async def main():
    # Start the bot
    await dp.start_polling(bot)


asyncio.run(main())