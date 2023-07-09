import requests
import sys
import datetime
import json
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

args = sys.argv
headers = {'X-Api-Key': f'{args[1]}'}
my_share = share.Share('4689.T')
symbol_data = None
# 30日分の株価の1日の最高値を取得(終値が1日の中でも動いているの、1時間おきの終値って考えたら納得できそう)
try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                          30,
                                          share.FREQUENCY_TYPE_MINUTE,
                                          5)
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

# symbol_data['high']の中にNoneが含まれていて、そのままだとうまく最小値がとれないので、filterをかける
filtered_high = filter(lambda x: x is not None, symbol_data['high'])
filtered_low = filter(lambda x: x is not None, symbol_data['low'])
min_value = min(filtered_low)
max_value = max(filtered_high)
for timestamp, high, low in zip(symbol_data['timestamp'], symbol_data['high'], symbol_data['low']):
    if high == max_value:
        max_timestamp = timestamp
    if low == min_value:
        min_timestamp = timestamp

max_date=datetime.datetime.fromtimestamp(int(max_timestamp/1000)).strftime('%Y-%m-%d')
min_date=datetime.datetime.fromtimestamp(int(min_timestamp/1000)).strftime('%Y-%m-%d')
print("MAX:", max_date, ",", max_value)
print("MIN:", min_date, ",", min_value)

def get_article_titles(date):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'ヤフー OR Zホールディングス',
        'sortBy': 'popularity',
        'from': f'{date}',
        'to': f'{date}'
    }
    response = requests.get(url, headers=headers, params=params).json()
    titles = []
    for article in response['articles']:
        title = article['title']
        titles.append(title)
    return titles

print("ARTICLE_MIX_VALUE:")
min_titles = get_article_titles(min_date)
print(min_titles)

print("ARTICLE_MAX_VALUE:")
max_titles = get_article_titles(max_date)
print(max_titles)
