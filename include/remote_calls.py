import json
import pickle
import smtplib
import requests
import pandas as pd
import numpy as np
from lxml import html
from datetime import date
from os import error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os.path

def get_boat_stats(ship_id: int) -> list:
#    url = f"https://api.cryptobay.top/bay/cryptobaygetobject?data=%7B%22token_type%22%3A1%2C%22\
#token_id%22%3A{ship_id}%2C%22with_powerpoints%22%3Atrue%2C%22with_level%22%3Atrue%7D"
    url = f"https://api.cryptobay.io/bay/cryptobaygetobject?data=%7B%22token_type%22%3A1%2C%22\
token_id%22%3A{ship_id}%2C%22with_powerpoints%22%3Atrue%2C%22with_level%22%3Atrue%7D"
    raw_json = requests.get(url).json()
    stats_list = []
    for stat in ['raw_space','raw_speed','raw_skill','raw_defence',\
        'raw_attack', 'raw_morale']:
        stats_list.append(int(raw_json['data'][stat]))
    return stats_list

class compute_price:
    def __init__(self, ship_id: int, resale_discount: float):
        self.model = pickle.load(open("db/model_BNB.sav", 'rb'))
        self.ship_id = ship_id
        self.resale_discount = resale_discount
        self.ship_stats = get_boat_stats(self.ship_id)
        self.ship_stats = np.array(self.ship_stats).reshape(1,-1)

    def predict(self):
        return round(float(self.model.predict(self.ship_stats)),3)

    def discounted_price(self):
        return round((self.predict() * self.resale_discount) * 0.95 - 0.002, 3)

def update_accounts():
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}
    columns = ['acc_id', 'sold', 'available']
    account_status_file = "db/accounts/account_status.csv"
    accounts_df = pd.DataFrame(columns=columns)
    tr_df = pd.read_csv('db/transactions/transactions_hist.csv')
    today = date.today().strftime("%Y-%m-%d")

    # Try to get last account_status.csv file to compare it to the new
    if os.path.isfile(account_status_file):
        accounts_df_old = pd.read_csv(account_status_file)
    else:
        accounts_df_old = ""
    
    with open('tools/conf.json') as f:
        acc_file = json.load(f)

    for i in range(1,6):
        acc_addr = acc_file[f'account{i}']
        page = requests.get(f"https://bscscan.com/address/{acc_addr}", headers=headers)
        tree = html.fromstring(page.content)

        raw_list = tree.xpath('//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/div[1]/div/div[2]/div[1]/div[2]/text()')
        sold = raw_list[0] + "." + raw_list[1].split()[0]
        sold = round(float(sold), 3)

        available = 1 if sold > 0.08 else 0         # IMPORTANT: account becomes available if sold > 0.08 BNB
        available = int(available)
        acc_series = pd.Series([i,sold,available], index=columns)
        accounts_df = accounts_df.append(acc_series, ignore_index=True)
        if(available == True):
            if(tr_df[tr_df['acc_id'] == i]['tr_type'].tail(1).values[0] == 'resell'):
                sell_line = tr_df[(tr_df['acc_id'] == i) & (tr_df['tr_type'] == 'resell')].tail(1)
                sell_line['tr_type'] = 'sell'
                sell_line['date'] = today
                tr_df = tr_df.append(sell_line, ignore_index=True)

    accounts_df = accounts_df.astype({'acc_id': 'int32', 'available': 'bool'})
    accounts_df.to_csv('db/accounts/account_status.csv', index=False)
    tr_df.to_csv('db/transactions/transactions_hist.csv', index=False)

    for i in range(1,6):
        if(accounts_df.loc[i-1,'available'] == True):
            if accounts_df.loc[i-1,'available']  != accounts_df_old.loc[i-1,'available']:
                send_email.on_boat_sale(send_email(),i)

class send_email():
    def __init__(self):
        self.gmail_user = 'miezuaa@gmail.com'

        with open("tools/zzsecrets.json") as self.f:
            self.data = json.load(self.f)
            self.gmail_password = self.data['GMAIL_APP_PASS']

            self.sent_from = self.gmail_user
            self.to = [self.gmail_user]
            self.msg = MIMEMultipart()
            self.msg['From'] = self.sent_from
    
    def on_boat_sale(self, acc_id):
        self.acc_id = acc_id
        self.df_accounts = pd.read_csv("db/accounts/account_status.csv")
        self.msg['subject'] = f'Account {self.acc_id} SOLD a boat'
        self.html = f"""
<html>
  <head></head>
  <body>
    {self.df_accounts.to_html(index=False)}
  </body>
</html>
        """
        self.send(self.html)

    def on_super_offer(self, df: pd.DataFrame, flip_ratio: float) -> callable:
        self.offer_df = df
        self.flip_ratio = flip_ratio
        self.msg['subject'] = f'Super offer found at flip ratio: {self.flip_ratio}'
        self.html = f"""
<html>
  <head></head>
  <body>
    {self.offer_df.to_html(index=False)}
  </body>
</html>
        """
        self.send(self.html)

    def send(self, html):
        self.html = html
        self.part1 = MIMEText(self.html, 'html')
        self.msg.attach(self.part1)

        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(self.gmail_user, self.gmail_password)
            self.server.sendmail(self.msg['From'], self.to, self.msg.as_string())
            self.server.close()

            print('Email sent!')
        except:
            print('Something went wrong...')

def get_sold_statistics():
    #https://api.cryptobay.top/bay/cryptobaygetauctionsummary?data=%7B%22timestamp%22%3A1636030119%7D
    pass

def get_binance_price_coinograph() -> int:
    """
    NOT USED. Limits API calls
    Example
            {
        "exchange": "binance",
        "pair": "bnbusdt",
        "price": 335.8,
        "ask": 335.8,
        "bid": 335.7
        }
    """
    price_json = requests.get("https://coinograph.io/ticker/?symbol=binance:bnbusdt").json()
    return price_json['price']

def get_binance_price_coingecko() -> float:
    """
    Example
    {'id': 'binancecoin',
    'symbol': 'bnb',
    'name': 'Binance Coin',
    'image': 'https://assets.coingecko.com/coins/images/825/large/binance-coin-logo.png?1547034615',
    'current_price': 400.07,
    'market_cap': 61889077351,
    'market_cap_rank': 5,
    'fully_diluted_valuation': 68296906490,
    'total_volume': 1565273152,
    'high_24h': 401.01,
    'low_24h': 372.01,
    'price_change_24h': 25.8,
    'price_change_percentage_24h': 6.89444,
    'market_cap_change_24h': 3991379311,
    'market_cap_change_percentage_24h': 6.89385,
    'circulating_supply': 154533651.9,
    'total_supply': 170533651.9,
    'max_supply': 170533651.9,
    'ath': 686.31,
    'ath_change_percentage': -41.64571,
    'ath_date': '2021-05-10T07:24:17.097Z',
    'atl': 0.0398177,
    'atl_change_percentage': 1005707.34064,
    'atl_date': '2017-10-19T00:00:00.000Z',
    'roi': None,
    'last_updated': '2021-10-01T08:23:03.665Z'}
    """
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=binancecoin"
    price_json = requests.get(url).json()[0]['current_price']
    return price_json