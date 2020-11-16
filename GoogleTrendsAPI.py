requirements.txt
git push heroku master
heroku buildpacks:clear
heroku buildpacks:add heroku/python

import os
import pickle
import time
import datetime
import pandas as pd
from pytrends.request import TrendReq
import random
import schedule

##get prices and other info using coingecko
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
# selected specific coins based on mcap, volume and popularity

coins = ['bitcoin', 'ethereum', 'eos', 'xrp', 'chainlink', 'binance coin', 'litecoin', 'cardano', 'monero', 'tron',
         'stellar', 'tezos', 'okb', 'nem', 'neo', 'iota',
         'dash', 'zcash', 'ethereum classic', 'maker', 'waves', 'ontology', 'zilliqa', 'syscoin', 'pivx', 'bluzelle',
         'qtum', 'icon', 'lisk', 'bitcoin gold', 'golem',
         'siacoin', 'stratis', 'verge', 'komodo', 'ark', 'steem', 'power ledger', 'wanchain', 'kleros', 'WaykiChain',
         'QuarkChain', 'Cindicator', 'Grin', 'Nebulas']

now = datetime.datetime.now()
n = random.randint(0,10)
def get_crypto_info(coins, sleep=n, save=False):   
    coins_price_btc = cg.get_coins_price(ids=coins, vs_currencies='btc',rice_change_percentage='1h')
    coins_market_price_usd = (cg.get_coins_markets(ids=coins, vs_currency='usd', price_change_percentage='1h'))
    coins_market_price_usd = pd.DataFrame(coins_market_price_usd)
    coins_price_btc = pd.DataFrame(coins_price_btc)
    time.sleep(sleep)
    if save:
        path = ('C:/Users/berta/Desktop/data analytics/mstr/getdata')
        save_path = os.path.abspath(os.path.join(path))
        file = '{}\PriceList_{}_{}.csv'.format(save_path, now.strftime('%m%d%y, %H'), 'hour')
        file2 = '{}\PriceList_btc{}_{}.csv'.format(save_path, now.strftime('%m%d%y, %H'), 'hour')
        coins_market_price_usd.to_csv(file, index=False, encoding='utf-8')
        coins_price_btc.to_csv(file2, index=False, encoding='utf-8')
        return coins_market_price_usd.head()

#schedule.every().hour.do(get_crypto_info(coins, save=False))

get_crypto_info(coins,save=True)
# The list of coins that were used to get the price are also used for trends.
#random numbers

# the following function could be used for daily trends however regarding hourly trends the second function seems to be more suitable which you can find below

def crypto_trends_fetcher(coins, start, end, sleep=n,save=False):
    coins = list(coins)
    CryptoTrend = TrendReq()
    AllCoinTrends = pd.DataFrame()
    CoinTrends = pd.DataFrame()
    for coin in coins[0: len(coins)]:
        try:
            CryptoTrend.build_payload(kw_list=[coin], timeframe='{} {}'.format(start, end))
            interest_coin = CryptoTrend.interest_over_time()
            interest_coin.rename(columns={coin: 'interest'}, inplace=True)
            interest_coin.insert(0, 'CoinName', coin)
            CoinTrends = CoinTrends.append(interest_coin)
        except Exception as e:
            print('unable to fetch {} trends data'.format(coin))
            print(e)

        time.sleep(sleep)  # Request at most 1 time per second to avoid request limits

        if save:
            save_path = os.path.abspath(os.path.join('C:/Users/berta/Desktop/data analytics/mstr/getdata'))
            file = '{}/CryptoTrends_{}_{}.csv'.format(save_path, start, end)
            AllCoinTrends.to_csv(file, encoding='utf-8')

        AllCoinTrends = AllCoinTrends.append(CoinTrends)

        return AllCoinTrends
    # trends can be obtained hourly within a specified time period, in this case I have set the running to be daily with current date.(# pytrends timezone is UCT, when setting the time, take UCT time zone into account)
now = datetime.datetime.now()
z = random.randint(0,10)
def crypto_hourly_trends_fetcher(coins, year_start=now.year, month_start=now.month, day_start=now.day, hour_start=0,
                                     year_end=now.year, month_end=now.month, day_end=now.day, hour_end=23, sleep=z, save=False):

    coins = list(coins)
    CryptoTrend = TrendReq()
    AllCoinTrendshourly = pd.DataFrame()
    CoinTrendshourly = pd.DataFrame()
    for coin in coins[0: len(coins)]:
        try:
            interest_coin = CryptoTrend.get_historical_interest([coin], year_start=year_start, month_start=month_start,
                                                                day_start=day_start, hour_start=hour_start,
                                                                year_end=year_end, month_end=month_end,
                                                                day_end=day_end, hour_end=hour_end)
            interest_coin.rename(columns={coin: 'interest'}, inplace=True)
            interest_coin.insert(0, 'CoinName', coin)
            CoinTrendshourly = CoinTrendshourly.append(interest_coin)
        except Exception as e:
            print('unable to fetch {} trends data'.format(coin))
            print(e)

        time.sleep(sleep)  # Request at most 1 time per second to avoid request limits

        AllCoinTrendshourly = AllCoinTrendshourly.append(CoinTrendshourly)
        if save:
            save_path2 = os.path.abspath(os.path.join('C:/Users/berta/Desktop/data analytics/mstr/getdata'))
            file = '{}/CryptoTrends_hourly{}.csv'.format(save_path2, now.day)
            AllCoinTrendshourly.to_csv(file, encoding='utf-8')

        return AllCoinTrendshourly
    
    crypto_hourly_trends_fetcher(coins,save=True)
