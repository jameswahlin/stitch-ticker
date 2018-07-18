#!/usr/bin/env python

import time
import requests
import scrolling_text

def get_quote(ticker):

    has_response = False
    while not has_response:
        url = "ADD URL HERE"
        payload = '{"ticker": "' + ticker + '"}';
        response = requests.post(url, data=payload, headers={"Content-Type": "application/json"})

        if not response.status_code == 200:
            #print(response.json())
            continue

        has_response = True
        quote = response.json()

        last_price = float(quote["price"])
        volume = int(quote["volume"])

        prev_close_price = float(quote["prevPrice"])
        percent_change = 100 * ((last_price - prev_close_price) / prev_close_price)

    return (last_price, volume, prev_close_price, percent_change)

def run():
    color_ticker = (255, 255, 255)
    color_flat = (255, 255, 255)
    color_up = (0, 255, 0)
    color_down = (255, 0, 0)

    while True:
        try:
            last_price, volume, prev_close_price, percent_change = get_quote("mdb")

            display_last_price = "{:.2f}".format(last_price)
            display_volume = "{:,}".format(volume)
            display_percent_change = "{0:.2f}".format(percent_change)

            lines = ["mdb", display_last_price, "%chg " +  display_percent_change,
                     "vol " + display_volume]

            price_color = color_flat
            if last_price > prev_close_price:
                price_color = color_up
            elif last_price < prev_close_price:
                price_color = color_down

            colors = [color_ticker, price_color, price_color, price_color]

            scrolling_text.display_text(lines, colors)
        except ValueError as valerr:
            print(valerr)
            time.sleep(1)
            continue
        except Exception as e:
            print (e)
            time.sleep(1)
            continue

run()
