import pyswagger
from pyswagger import App
from pyswagger.primitives import MimeCodec
from pyswagger.primitives.codec import PlainCodec
from esipy import App
from esipy import EsiClient
import json
import simplejson
from flask import url_for
from flask import request


mime_codec = MimeCodec()
mime_codec.register('text/html', PlainCodec())


#order_type = 'sell'
#type_id = 2268
#region_id = 10000002
#station = 60003760

app = App.create(url="https://esi.evetech.net/latest/swagger.json?datasource=tranquility")
client = EsiClient(
    retry_request=True,
    header={'User-Agent': 'Fetch Prices'},
    raw_body_only=False)


def fetch_orders(buy_sell, item, region):
    global app
    market_price_operation = app.op['get_markets_region_id_orders'](
        order_type=buy_sell,
        region_id=region,
        type_id=item
    )

    #returns a list of orders
    global client
    response = client.request(market_price_operation)
    return response

def extract_prices(response, station):
    i = 0
    price_list = []
    while True:
        try:
            price = response.data[i].price
            if(response.data[i].location_id == station):
                    price_list.append(price)
            i += 1
        except:
            return price_list

def find_price(order_type, type_id, region_id, station):
    order_list =  fetch_orders(order_type, type_id, region_id)
    prices = extract_prices(order_list, station)
    if order_type == "buy":
        try:
            return max(prices)
        except ValueError:
            print("No buy value found")
            return
    else:
        try:
            return min(prices)
        except ValueError:
            print("No sell value found")
            return

#print(find_price(order_type, type_id, region_id, station))

