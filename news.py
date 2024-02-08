import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time 
import json

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
        
        article_id = article_url.split('/')[-2]
        news_dict[article_id] = {
            'article_date_timestamp': article_date_timestamp,
            'article_title': article_title,
            'article_url': article_url,
        }

    with open('news_dict.json','w') as file:
        json.dump(news_dict,file,indent=4,ensure_ascii=False)

def main():
    get_first_news()

if  __name__ == '__main__':
    main()