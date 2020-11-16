import os
import pickle
import time
import datetime
import pandas as pd
from pytrends.request import TrendReq
import schedule

##get prices and other info using coingecko
#from pycoingecko import CoinGeckoAPI

#cg = CoinGeckoAPI()
#selected specific coins based on mcap, volume and popularity 

coins = ['bitcoin', 'ethereum', 'eos','xrp','chainlink','binance coin','litecoin','cardano','monero','tron','stellar','tezos','okb','nem','neo','iota',
         'dash','zcash','ethereum classic','maker','waves','ontology','zilliqa','syscoin','pivx','bluzelle','qtum','icon','lisk','bitcoin gold','golem',
         'siacoin','stratis','verge','komodo','ark','steem','power ledger','wanchain','kleros','WaykiChain','QuarkChain','Cindicator','Grin','Nebulas']


#def get_crypto_info(coins, sleep=3, save=False):
    # price of coins w.r.t bitcoin
 #   coins_price_btc = cg.get_price(ids=coins, vs_currencies='btc')
    # price and additional market data for listed coins
  #  coins_market_price_usd = (cg.get_coins_markets(ids=coins, vs_currency='usd', price_change_percentage='1h'))
   # coins_market_price_usd = pd.DataFrame(coins_market_price_usd)
    #coins_price_btc = pd.DataFrame(coins_price_btc)
    #time.sleep(sleep)
    #if save:
     #   path = '..../data'
      #  now = datetime.now()
       # save_path = os.path.abspath(os.path.join(path))
       # file = '{}\PriceList_{}_{}.csv'.format(save_path, now.strftime('%m%d%y, %H'), 'hour')
       # file2 = '{}\PriceList_btc{}_{}.csv'.format(save_path, now.strftime('%m%d%y, %H'), 'hour')
       # coins_market_price_usd.to_csv(file, index=False, encoding='utf-8')
        #coins_price_btc.to_csv(file2, index=False, encoding='utf-8')
    #return coins_market_price_usd.head()

#schedule.every().hour.do(get_crypto_info(coins, save=False))


#The list of coins that were used to get the price are also used for trends. 

#the following function could be used for daily trends however regarding hourly trends the second function seems to be more suitable which you can find below 
def crypto_trends_fetcher(coins, start, end, sleep=3):
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
            save_path = os.path.abspath(os.path.join('../data'))
            file = '{}/CryptoTrends_{}_{}.csv'.format(save_path, start, end)
            AllCoinTrends.to_csv(file, encoding='utf-8')

         AllCoinTrends = AllCoinTrends.append(CoinTrends)

        return AllCoinTrends
    #trends can be obtained hourly within a specified time period, in this case I have set the running to be daily with current date.(# pytrends timezone is UCT, when setting the time, take UCT time zone into account)   
    def crypto_hourly_trends_fetcher(coins, year_start=now.year, month_start=now.month, day_start=now.day, hour_start=0, year_end=now.year, month_end=now.month, day_end=now.day, hour_end=23, sleep=10):
    now = datetime.datetime.now()
    coins = list(coins)
    CryptoTrend = TrendReq()
    AllCoinTrends = pd.DataFrame()
    CoinTrends = pd.DataFrame()
    for coin in coins[0: len(coins)]:
        try:
            interest_coin=CryptoTrend.get_historical_interest([coin], year_start=year_start,month_start=month_start,
                                                              day_start=day_start, hour_start=hour_start,year_end=year_end, month_end=month_end,
                                                              day_end=day_end, hour_end=hour_end)
            interest_coin.rename(columns={coin: 'interest'}, inplace=True)
            interest_coin.insert(0, 'CoinName', coin)
            CoinTrends = CoinTrends.append(interest_coin)
        except Exception as e:
            print('unable to fetch {} trends data'.format(coin))
            print(e)

        time.sleep(sleep)  # Request at most 1 time per second to avoid request limits

         AllCoinTrends = AllCoinTrends.append(CoinTrends)
             
                if save:
            save_path = os.path.abspath(os.path.join('../data'))
            file = '{}/CryptoTrends_{}.csv'.format(save_path,now.day)
            AllCoinTrends.to_csv(file, encoding='utf-8')

        return AllCoinTrends
