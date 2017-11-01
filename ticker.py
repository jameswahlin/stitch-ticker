import json
import requests
import scrolling_text
import time

def getTickerList():
  url = "https://stitch.mongodb.com/api/client/v1.0/app/mdb-ticker-hplox/svc/ConfigView/incomingWebhook/59f8b7ae058429a3914d6f15?secret=abcd"
  response = requests.get(url).json()
  data = response["tickerList"]

  #print(data)

  tickerList = data.split(",")

  return tickerList


def getQuote(ticker):

  hasResponse = False
  while (not hasResponse):
    # url = "https://stitch.mongodb.com/api/client/v1.0/app/mdb-ticker-hplox/svc/GetQuote/incomingWebhook/59f798534fdd1fc4e6c58d17?secret=abcd"
    # response = requests.get(url).json()

    url = "https://stitch.mongodb.com/api/client/v1.0/app/mdb-ticker-hplox/svc/GetQuoteForTicker/incomingWebhook/59f9d66046224c60567145be?secret=abcd"
    payload = '{"ticker": "' + ticker + '"}'
    response = requests.post(url, data=payload, headers={"Content-Type": "application/json"}).json()

    if not "body" in response:
      print(response)
      continue

    data = response["body"]
    hasResponse = True

  dailyQuotes = data.splitlines()

  currentQuote = dailyQuotes[1].split(",")
  previousQuote = dailyQuotes[2].split(",")

  date = currentQuote[0]
  openPrice = float(currentQuote[1])
  highPrice = float(currentQuote[2])
  lowPrice = float(currentQuote[3])
  closePrice = float(currentQuote[4])
  volume = int(currentQuote[5])

  prevClosePrice = float(previousQuote[4])
  percentChange = 100 * ((closePrice - prevClosePrice) / prevClosePrice)

  return (date, openPrice, closePrice, volume, prevClosePrice, percentChange)


colorTicker = (255, 255, 255)
colorFlat = (255, 255, 255)
colorUp = (0, 255, 0)
colorDown = (255, 0, 0)

while True:
  tickerList = getTickerList()

  if len(tickerList) == 1 and tickerList[0] == "pause":
    time.sleep(1)
    continue

  for ticker in tickerList:
    date,openPrice,lastPrice,volume,prevClosePrice,percentChange = getQuote(ticker)

    displayLastPrice = "{:.2f}".format(lastPrice)
    displayVolume = "{:,}".format(volume)
    displayPercentChange = "{0:.2f}".format(percentChange)

    lines = [ticker, displayLastPrice, "%chg " + displayPercentChange, "vol " + displayVolume]

    priceColor = colorFlat
    if lastPrice > prevClosePrice:
        priceColor = colorUp
    elif lastPrice < prevClosePrice:
        priceColor = colorDown

    colors = [colorTicker, priceColor, priceColor, priceColor]

    scrolling_text.display_text(lines, colors)