#!/usr/bin/env python

import time

import requests
import scrolling_text

def get_ticker_list():
    url = "https://stitch.mongodb.com/api/client/v1.0/app/mdb-ticker-hplox/svc/ConfigView/incomingWebhook/59f8b7ae058429a3914d6f15?secret=abcd"
    response = requests.get(url).json()
    data = response["tickerList"]

    #print(data)

    return data.split(",")

def get_quote(ticker):

    has_response = False
    while not has_response:
        url = "https://stitch.mongodb.com/api/client/v1.0/app/mdb-ticker-hplox/svc/GetQuoteForTicker/incomingWebhook/59f9d66046224c60567145be?secret=abcd"
        payload = '{"ticker": "' + ticker + '"}'
        response = requests.post(url, data=payload, headers={"Content-Type": "application/json"})

        if not response.status_code == 200:
            #print(response.json())
            continue

        has_response = True
        data = response.json()["body"]

        if data.find("Error Message") >= 0:
            raise ValueError("Invalid ticker: " + ticker)

    daily_quotes = data.splitlines()

    current_quote = daily_quotes[1].split(",")
    previous_quote = daily_quotes[2].split(",")

    close_price = float(current_quote[4])
    volume = int(current_quote[5])

    prev_close_price = float(previous_quote[4])
    percent_change = 100 * ((close_price - prev_close_price) / prev_close_price)

    return (close_price, volume, prev_close_price, percent_change)

def run():
    color_ticker = (255, 255, 255)
    color_flat = (255, 255, 255)
    color_up = (0, 255, 0)
    color_down = (255, 0, 0)

    while True:
        ticker_list = get_ticker_list()

        if len(ticker_list) == 1 and ticker_list[0] == "pause":
            time.sleep(1)
            continue
        try:
            for ticker in ticker_list:
                last_price, volume, prev_close_price, percent_change = get_quote(ticker)

                display_last_price = "{:.2f}".format(last_price)
                display_volume = "{:,}".format(volume)
                display_percent_change = "{0:.2f}".format(percent_change)

                lines = [ticker, display_last_price, "%chg " + display_percent_change,
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

run()
