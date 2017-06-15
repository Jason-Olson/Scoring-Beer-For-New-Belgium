from pymongo import MongoClient
import requests
from urllib import request
import json



def get_data():
    new_data = request.urlopen('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').read()


    # try:
    #     bitstamp = requests.get(
    #         'https://www.bitstamp.net/api/v2/ticker/btcusd/')
    #     results['bitstamp'] = float(bitstamp.json()['bid'])
    #     kraken = requests.get(
    #         'https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
    #     results['kraken'] = float(kraken.json()['result']['XXBTZUSD']['a'][0])
    #     bittrex = requests.get(
    #         'https://bittrex.com/api/v1.1/public/getticker?market=usdt-btc')
    #     results['bittrex'] = bittrex.json()['result']['Bid']
    #     return results
    # except:
    #     return False


# def get_lowest_rate(rates):
#     lowest = min(rates, key=rates.get)
#     new_rates = []
#     for key, value in rates.items():
#         new = {'currency': key, 'price': value, 'lowest': False}
#         if key == lowest:
#             new['lowest'] = True
#         new_rates.append(new)
#     return new_rates


def add_data(data):
    client = MongoClient()
    db = client.fraud_db
    coll = db.fraud_coll
    post_id = coll.insert_one(data).inserted_id
