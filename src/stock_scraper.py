"""
This only works for US stocks on the NASDAQ for dividends, doesn't contain Canadian
"""

import json
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--secrets",
					type=str,
					help="File containing for API keys",
					default="keys.json",
					required=False)
parser.add_argument("--ticker",
					type=str,
					help="Ticker symbol for stock. If on TSX suffix with .to")
args = parser.parse_args()


class StockScraper:
	def __init__(self, ticker, secrets_filename):
		self._ticker = ticker

		with open(secrets_filename) as json_file:
			self._secret_data = json.load(json_file)

		self._time_series_url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol="
		self._api_key_url = "&apikey="

		self._url = "%s%s%s%s" % (self._time_series_url, self._ticker, self._api_key_url, self._secret_data['ALPHA_VANTAGE_API_KEY'])

	def request_time_series_data(self):
		response = requests.get(self._url)
		res_json = response.json()
		print(res_json)
		exit()
		# return res_json['Time Series (Daily)']

	def get_dividend_data(self, time_series_data):
		dividend_payments = []
		for key, value in time_series_data.items():
			div_amt = float(value['7. dividend amount'])
			print (div_amt)
			if div_amt > 0:
				print("Got number", div_amt)
				exit()


if __name__ == "__main__":
	div_scraper = StockScraper(secrets_filename=args.secrets, ticker=args.ticker)
	time_series_data = div_scraper.request_time_series_data()

	div_data = div_scraper.get_dividend_data(time_series_data)
