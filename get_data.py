import requests
import re
import random
from datetime import datetime

descriptors = {"up": ["up", "soaring", "very good", "positively amazing", "soars"], "down": ["down", "falls", "crashes", "tanks", "plummets"]}

stocks_headers = {
    'Accept':'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.londonstockexchange.com/',
    'Origin': 'https://www.londonstockexchange.com',
    'User-Agent': 'BrandisNewsAndStockScraper',
    'DNT': '1',
    'Sec-GPC': '1',
    'Sec-Fetch-Mode': 'cors',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

request = requests.get('https://api.londonstockexchange.com/api/v1/pages?path=ftse-index&parameters=indexname%253Dftse-100', headers=stocks_headers)

stock_change = request.json()['components'][2]['content'][0]['value'][0]['percentualchange']

if (stock_change > 0):
    stock_descriptor = random.choice(descriptors["up"])
elif (stock_change < 0):
    stock_descriptor = random.choice(descriptors["down"])
else:
    stock_descriptor = "doing nothing"

request = requests.get('https://feeds.bbci.co.uk/news/rss.xml')

headline = random.choice(re.findall(r"<title>(.*?)</title>", request.text.replace("<![CDATA[", "").replace("]]>", "").replace("<title>BBC News</title>", "")))


path = "/var/www/news-and-stocks-fun/index.html"
with open(path, "w") as index:
    index.write(f'''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="Tom Brandis website homepage">
            <title>The Financial Headline Generator by Tom Brandis</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <p>
                Stock market
                <span id="market_direction">{stock_descriptor}</span>
                as
                <span id="news_headline">{headline}</span>
            </p>
            <p id="credits">Inspired by <a href="https://www.smbc-comics.com/comic/markets">SMBC 'markets'</a>. Data from <a href="https://www.londonstockexchange.com">London stack exchange</a> and <a href="https://www.bbc.co.uk/">BBC News</a>. For entertainment only - data is out of date. Page generated on {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </body>
    </html>
    ''')
