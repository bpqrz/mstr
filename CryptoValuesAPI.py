import pandas as pd
import schedule

##get prices and other info using coingecko
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
#selected specific coins based on mcap, volume and popularity 
coins = ['bitcoin', 'ethereum', 'eos','xrp','chainlink','binance coin','litecoin','cardano','monero','tron','stellar','tezos','okb','nem','neo','iota',
         'dash','zcash','ethereum classic','maker','waves','ontology','zilliqa','syscoin','pivx','bluzelle','qtum','icon','lisk','bitcoin gold','golem',
         'siacoin','stratis','verge','komodo','ark','steem','power ledger','wanchain','kleros','WaykiChain','QuarkChain','Cindicator','Grin','Nebulas']


def get_crypto_info(coins, sleep=3, save=False):
    # price of coins w.r.t bitcoin
    coins_price_btc = cg.get_price(ids=coins, vs_currencies='btc')
    # price and additional market data for listed coins
    coins_market_price_usd = (cg.get_coins_markets(ids=coins, vs_currency='usd', price_change_percentage='1h'))
    coins_market_price_usd = pd.DataFrame(coins_market_price_usd)
    coins_price_btc = pd.DataFrame(coins_price_btc)
    time.sleep(sleep)
    if save:
        path = '..../data'
        now = datetime.now()
        save_path = os.path.abspath(os.path.join(path))
        file = '{}\PriceList_{}_{}.csv'.format(save_path, now.strftime('%m%d%y, %H'), 'hour')
        file2 = '{}\PriceList_btc{}_{}.csv'.format(save_path, now.strftime('%m%d%y, %H'), 'hour')
        coins_market_price_usd.to_csv(file, index=False, encoding='utf-8')
        coins_price_btc.to_csv(file2, index=False, encoding='utf-8')
    return coins_market_price_usd.head()

schedule.every().hour.do(get_crypto_info(coins, save=False))
