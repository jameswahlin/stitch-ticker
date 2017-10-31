import requests
import scrolling_text
import time

def getQuote():
  url = "https://stitch.mongodb.com/api/client/v1.0/app/mdb-ticker-hplox/svc/GetQuote/incomingWebhook/59f798534fdd1fc4e6c58d17?secret=abcd"
  response = requests.get(url).json()

  data = response[0]["body"]

  print(data)

  dailyQuotes = data.splitlines()

  currentQuote = dailyQuotes[1].split(",")

  date = currentQuote[0]
  openPrice = currentQuote[1]
  highPrice = currentQuote[2]
  lowPrice = currentQuote[3]
  closePrice = currentQuote[4]
  volume = currentQuote[5]

  return (date, openPrice, closePrice, volume)

while True:
  date,openPrice,lastPrice,volume = getQuote()

  lines = ["NASDAQ:MDB", lastPrice, "{:,}".format(int(volume))]

  colorTicker = (255, 255, 255)
  colorFlat = (255, 255, 255)
  colorUp = (0, 255, 0)
  colorDown = (255, 0, 0)

  priceColor = colorFlat
  if float(lastPrice) > float(openPrice):
      priceColor = colorUp
  elif float(lastPrice) < float(openPrice):
      priceColor = colorDown

  colors = [colorTicker, priceColor, priceColor]

  scrolling_text.display_text(lines, colors)