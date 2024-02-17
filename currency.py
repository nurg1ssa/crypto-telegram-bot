from bs4 import BeautifulSoup
from aiogram.utils.markdown import hbold
import requests

async def price():
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
    return price_message