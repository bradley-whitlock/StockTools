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
		self.ticker = ticker

		with open(secrets_filename) as json_file:
			self.secret_data = json.load(json_file)

		self.time_series_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="
		self.api_key_url = "&apikey="

		self.url = "%s%s%s%s" % (self.time_series_url, self.ticker, self.api_key_url, self.secret_data['ALPHA_VANTAGE_API_KEY'])

	def get_data(self):
		response = requests.get(self.url)
		res_json = response.json()
		print(res_json)


if __name__ == "__main__":
	div_scraper = StockScraper(secrets_filename=args.secrets, ticker=args.ticker)
	div_scraper.get_data()
