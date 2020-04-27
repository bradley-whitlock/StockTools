import json
import numpy as np
import requests

from common import *


class StockUtils:
	def __init__(self, ticker, secrets, start_date):
		self._ticker = ticker
		self._start_date = to_date_object(start_date, format="%Y-%m-%d")

		# For the stock price data
		self._time_series_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
		with open(secrets) as json_file:
			self._secret_data = json.load(json_file)
		self._stock_price_url = "%s%s.TO&apikey=%s&outputsize=full" % (self._time_series_url, self._ticker.upper(), self._secret_data['ALPHA_VANTAGE_API_KEY'])

		self.data = self.get_closing_prices()

	def get_closing_prices(self):
		response = requests.get(self._stock_price_url)
		res_json = response.json()
		time_series = res_json['Time Series (Daily)']
		closing_prices_stamped = []
		for day, prices in time_series.items():
			day_obj = to_date_object(day, format="%Y-%m-%d")
			if day_obj < self._start_date:
				continue
			closing_price = float(prices['4. close'])

			closing_prices_stamped.append([day_obj, closing_price])

		closing_prices_stamped.reverse()

		return np.array(closing_prices_stamped).T

	def monthly_stats(self):
		"""Returns a nx3 array with month, average price and std dev of price"""
		prices_for_range = []
		prices = []
		for idx in range(0, len(self.data[0])):
			if idx > 0 and self.data[0][idx].month != self.data[0][idx - 1].month:
				first = self.data[0][idx - 1]
				first = first.replace(day=1)
				prices = np.array(prices)
				prices_for_range.append([first, np.mean(prices), np.std(prices)])
				prices = []
			prices.append(self.data[1][idx])

		return np.array(prices_for_range).T


