import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time 
import os
import json
from subscription.subscriptions_manager import SubscriptionsManager
from aiogram.utils.markdown import hbold, hlink


db = SubscriptionsManager('./subscription/subscriptions.db')


def get_first_news():
    headers = {
         'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    url = 'https://www.newsbtc.com/news/'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    jeg_posts = soup.find_all('article', class_='jeg_post')


    news_dict = {}

    for article in jeg_posts:
        article_title = article.find(class_= 'jeg_post_title').text.strip()

        # Extract the <a> tag inside <div class="jeg_thumb">
        a_tag = article.find('div', class_='jeg_thumb').find('a')
        # Check if the <a> tag is found
        if a_tag:
        # Extract the value of the href attribute
            article_url = a_tag.get('href')
        else:
            print("No <a> tag found within <div class='jeg_thumb'>")

        article_date = article.find('div', class_= 'jeg_meta_date').text.strip()
        date_from_str = datetime.strptime(article_date, "%B %d, %Y")
        article_date_timestamp = time.mktime(date_from_str.timetuple())
        article_div = article.find("div", class_="thumbnail-container").find('img')  # Find the div containing the image
        if article_div:
            article_img =  article_div.get('data-src')
        else:
            article_img = article.find("div", class_="thumbnail-container").get('data-src')
        article_id = article_url.split('/')[-2]
        news_dict[article_id] = {
            'article_date_timestamp': article_date_timestamp,
            'article_title': article_title,
            'article_url': article_url,
            'article_image': article_img,
        }

    with open('./parsing/news_dict.json','w') as file:
        json.dump(news_dict,file,indent=4,ensure_ascii=False)

def check_news_update():
    with open('./parsing/news_dict.json') as file:
        news_dict = json.load(file)
    headers = {
         'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    url = 'https://www.newsbtc.com/news/'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    jeg_posts = soup.find_all('article', class_='jeg_post')
    fresh_news = {}
    for article in jeg_posts:
        a_tag = article.find('div', class_='jeg_thumb').find('a')
        article_url = a_tag.get('href')
        article_id = article_url.split('/')[-2]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find(class_= 'jeg_post_title').text.strip()

            article_date = article.find('div', class_= 'jeg_meta_date').text.strip()
            date_from_str = datetime.strptime(article_date, "%B %d, %Y")
            article_date_timestamp = time.mktime(date_from_str.timetuple())
            article_div = article.find("div", class_="thumbnail-container").find('img')  # Find the div containing the image

            if article_div:
                article_img =  article_div.get('data-src')
            else:
                article_img = article.find("div", class_="thumbnail-container").get('data-src')

            news_dict[article_id] = {
                'article_date_timestamp': article_date_timestamp,
                'article_title': article_title,
                'article_url': article_url,
                'article_image': article_img,

            }
            fresh_news[article_id] = {
                'article_date_timestamp': article_date_timestamp,
                'article_title': article_title,
                'article_url': article_url,
                'article_image': article_img,
            }
    with open('./parsing/news_dict.json','w') as file:
        json.dump(news_dict,file,indent=4,ensure_ascii=False)
    return fresh_news

async def news_every_minute(bot):
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            print("Fresh news found:", fresh_news)  # Print fresh news for debugging
            for k, v in sorted(fresh_news.items()):
                formatted_date = datetime.fromtimestamp(v['article_date_timestamp']).strftime('%d.%m.%Y')
                caption = f"<b>{formatted_date}</b>\n\n{hbold(v['article_title'])}\n\n{hlink('Read More', v['article_url'])}"
                subscribers = db.get_subscriptions()
                print("Subscribers:", subscribers)  # Print subscribers for debugging
                for subscriber in subscribers:
                    try:
                        print("Sending message to:", subscriber[1])  # Print subscriber for debugging
                        await bot.send_photo(subscriber[1], v['article_image'], caption=caption, disable_notification=False, parse_mode="HTML")
                        print("Message sent successfully.")
                    except Exception as e:
                        print(f"Error sending message: {e}")

        await asyncio.sleep(60)


def main():
    # get_first_news()
    print(check_news_update())

if  __name__ == '__main__':
    main()