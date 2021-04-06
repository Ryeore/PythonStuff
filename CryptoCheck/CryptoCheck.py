# /usr/bin/python3
# https://www.bitstamp.net/api/v2/ticker/
import requests
import json
from time import sleep


def getBitcoinPrice():
    urlBTC = "https://www.bitstamp.net/api/v2/ticker/btcusd"
    try:
        r = requests.get(urlBTC)
        priceFloat = float(json.loads(r.text)["last"])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Bitstamp API")


def getEtherPrice():
    urlETH = "https://www.bitstamp.net/api/v2/ticker/ethusd"
    try:
        r = requests.get(urlETH)
        priceFloat = float(json.loads(r.text)["last"])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Bitstamp API")


def main(thr):
    while True:
        try:
            if float(thr) < getBitcoinPrice():
                print("ABOVE THRESHOLD!!! price: $" + str(getBitcoinPrice()) + " /BTC")
            else:
                print("Last price: $" + str(getBitcoinPrice()) + " /BTC")
            print("Last price: $" + str(getEtherPrice()) + " /ETH\n")
            sleep(10)
        except ValueError:
            print("Last price: $" + str(getBitcoinPrice()) + " /BTC")
            print("Last price: $" + str(getEtherPrice()) + " /ETH\n")
            sleep(10)


if __name__ == "__main__":
    val = input("Set threshold: ")
    main(val)
