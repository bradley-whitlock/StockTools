"""
This only works for Canadian stock on the TSX
"""
import pdb

import matplotlib.pyplot as plt
import numpy as np
import argparse

from canadian_dividend_utils import CanadianDividendUtils
from stock_utils import StockUtils
from common import *

parser = argparse.ArgumentParser()
parser.add_argument("--ticker",
					"-t",
					type=str,
					help="Ticker symbol for stock on the TSX")
parser.add_argument("--secrets",
					type=str,
					help="File containing for API keys",
					default="keys.json",
					required=False)
parser.add_argument("--start-date",
					"-s",
					type=str,
					required=False,
					help="Starting date, format: Year-Month-Day")
args = parser.parse_args()


class Stocks:
	def __init__(self, ticker, start_date, secrets):
		self._ticker = ticker
		self._start_date = to_date_object(start_date, format="%Y-%m-%d")

		self._page_load_timeout = 10
		self._data_dir = "data"

		self.dividend = CanadianDividendUtils(ticker=ticker, start_date=start_date)
		self.stock = StockUtils(ticker=ticker, secrets=secrets, start_date=start_date)

	def plot_dividend_deltas_with_stock_price(self):
		# First Subplot
		fig, axs = plt.subplots(1, 2)

		ax1 = axs[0]
		ax1.set_title("Dividend Payments for: %s" % self._ticker.upper())

		div_color = "tab:blue"
		div_date = self.dividend.data[0]
		div_amt = self.dividend.data[1]
		ax1.plot(div_date, div_amt, color=div_color)
		ax1.set_ylabel("Dividend Amount ($)", color=div_color)
		ax1.set_xlabel("Payment Date")
		ax1.tick_params(axis='y', labelcolor=div_color)
		ax1.set_ylim(bottom=0)

		ax2 = ax1.twinx()
		stock_color = 'tab:red'
		stock_date = self.stock.data[0]
		stock_amt = self.stock.data[1]
		ax2.plot(stock_date, stock_amt, color=stock_color, linewidth=0.6)
		ax2.tick_params(axis='y', labelcolor=stock_color)
		ax2.set_ylabel("Stock Price ($)", color=stock_color)
		ax2.set_ylim(bottom=0)

		# Second Subplot
		prev = div_amt[:-4]
		curr = div_amt[4:]
		deltas = np.divide(curr - prev, prev) * 100

		axs[1].plot(div_date[4:], deltas)
		axs[1].set_title("Dividend Delta's for: %s" % self._ticker.upper())
		axs[1].set_xlabel("Payment Date")
		axs[1].set_ylabel("% Change (1 year)")
		axs[1].grid()

		plt.tight_layout()
		plt.savefig("./plots/%s_dividend.png" % self._ticker)
		plt.show()

	def plot_stock_monthly(self):
		stats = self.stock.monthly_stats()
		month = stats[0]
		price_avg = stats[1]
		price_std = stats[2]

		plt.errorbar(month, price_avg, yerr=price_std, label='')
		plt.title("Monthly Stock Price with Volatility: %s" % self._ticker.upper())
		plt.xlabel("Payment Date")
		plt.ylabel("Amount ($)")
		plt.savefig("./plots/%s_monthly.png" % self._ticker)
		plt.show()


if __name__ == "__main__":
	stocks = Stocks(ticker=args.ticker, start_date=args.start_date, secrets=args.secrets)

	# stocks.plot_stock_monthly()
	stocks.plot_dividend_deltas_with_stock_price()
