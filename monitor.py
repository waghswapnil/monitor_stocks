#!/usr/bin/env python
# This script reads a json file from network and alerts if stock price is
# above or below the specified limits.
# The json file can be modified while the script is running to add more
# conditions.
# Source of data is google finance
# Runs in foreground for now.. Use Ctrl+C to exit.


import urllib2
import json
import sys
import time
import os


def get_quote(symbol, exchange):
    prefix = "http://finance.google.com/finance/info?client=ig&q=%s:%s"
    url = prefix % (exchange, symbol)
    content = urllib2.urlopen(url).read()
    return json.loads(content[3:])[0]


def notify_user(message, to_email):
    import smtplib
    from email.mime.text import MIMEText

    print("notify:" + message)

    username = str(os.environ['EMAIL_USER'])
    password = str(os.environ['EMAIL_PASSWORD'])

    msg = MIMEText(message)
    msg['Subject'] = message
    msg['From'] = username
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)

    server.sendmail(username, to_email, msg.as_string())
    server.quit()


class Stock:
    def __init__(self, symbol, exchange):
        self.symbol = symbol
        self.exchange = exchange

    def get_price(self):
        quote = get_quote(self.symbol, self.exchange)
        if not quote:
            raise "Symbol %s:%s does not exist" % (self.exchange, self.symbol)
        return float(quote['l'])

    def monitor(self, threshold_higher, threshold_lower, to_email):
        print("fetching price")
        price = self.get_price()
        print(price)
        if price < threshold_lower:
            notify_user("%s:%s=[%s] is below %s" % (self.exchange,
                                                    self.symbol,
                                                    price,
                                                    threshold_lower),
                        to_email)
        if price > threshold_higher:
            notify_user("%s:%s=[%s] is above %s" % (self.exchange,
                                                    self.symbol,
                                                    price,
                                                    threshold_higher),
                        to_email)


def monitor():
    for rule in rules:
        stock = Stock(rule['symbol'], rule['exchange'])
        stock.monitor(rule['high'], rule['low'], rule['email'])


rules_url = 'https://gist.githubusercontent.com/vvb/7606bf8e35074953987ddbdaa9f01d59/raw/rules.json'

while True:
    try:
        rules = json.loads(urllib2.urlopen(rules_url).read())
        monitor()
        time.sleep(300)
        sys.stdout.flush()
    except Exception as e:
        print(e)
        pass
