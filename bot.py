import logging
import os
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from bs4 import BeautifulSoup
import requests
from subscriptions_manager import SubscriptionsManager
from aiogram.utils.markdown import hbold, hlink
from news import check_news_update

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

db = SubscriptionsManager('subscriptions.db')


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    # Send a welcome message when users start interacting with the bot
    await message.answer("""
    👋 Hello and welcome to the Bitcoin Monitor Bot! 🚀

I'm here to keep you updated on the latest Bitcoin prices and provide valuable insights into the cryptocurrency market. Whether you're a seasoned investor or just curious about Bitcoin, I've got you covered!

💰 **Current Bitcoin Price:**
Just type /price to get the most recent Bitcoin price.

📰 **Newsletter Subscription:**
Subscribe to our newsletter with /subscribe to receive the latest news and updates in the cryptocurrency world.
Unsubscribe from the newsletter anytime using /unsubscribe.

Feel free to explore the various commands, and don't hesitate to ask if you have any questions. Happy monitoring! 🌐💰
    """)

@dp.message(Command('subscribe'))
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # If the user is not in the database, add them
        db.add_subscriber(message.from_user.id)
    else:
        # If they already exist, update their subscription status
        db.update_subscription(message.from_user.id, True)
    
    await message.answer("You have successfully subscribed to the newsletter! \nStay tuned, new reviews will be released soon, and you will be the first to know about them =)")

@dp.message(Command('unsubscribe'))
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # If the user is not in the database, add them with an inactive subscription
        db.add_subscriber(message.from_user.id, False)
        await message.answer("You are not subscribed anyway.")
    else:
        # If they already exist, update their subscription status
        db.update_subscription(message.from_user.id, False)
        await message.answer("You have successfully unsubscribed from the newsletter.")


@dp.message(Command('price'))
async def price(message: types.Message):
    headers = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    url = 'https://www.binance.com/en'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    prices = soup.find_all('a', class_='css-sujoqu')
    price_message = "<b>Cryptocurrency Prices:</b>\n\n"
    for price in prices:
        cryptoName = price.find('div', class_='css-1ev4kiq').text.strip()
        # Make cryptoName bold
        cryptoName_bold = hbold(cryptoName)
        cryptoPrice = price.find('div', class_='coinRow-coinPrice').text.strip()
        cryptoGrowth = price.find('div', class_='css-k2pbmh').text.strip()
        # Append crypto information to the message
        price_message += f"{cryptoName_bold}: {cryptoPrice}({cryptoGrowth})\n\n"
    
    # Send the message
    await message.answer(price_message, parse_mode="HTML")



async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                # Format the date
                formatted_date = datetime.datetime.fromtimestamp(v['article_date_timestamp']).strftime('%d.%m.%Y')

                # Create the HTML-like formatted caption
                caption = f"<b>{formatted_date}</b>\n\n{hbold(v['article_title'])}\n\n{hlink('Read More', v['article_url'])}"

                # Send the message with the photo and caption
                subscribers = db.get_subscriptions()
                for subscriber in subscribers:
                    try:
                        await bot.send_photo(subscriber[1], v['article_image'], caption=caption, disable_notification=False, parse_mode="HTML")
                    except Exception as e:
                        print(f"Error sending message: {e}")

        await asyncio.sleep(40)

async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())