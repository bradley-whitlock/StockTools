"""
This only works for Canadian stock on the TSX
"""
import pdb
import csv
from os import path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import matplotlib.pyplot as plt
import numpy as np
import datetime


class Scraper:
	def __init__(self, ticker):
		self._ticker = ticker
		self._base_url = "https://www.canadastockchannel.com/profile/?symbol="
		self._url = "%s%s" % (self._base_url, self._ticker)

		self._page_load_timeout = 10
		self._filename = "%s_dividends.csv" % self._ticker

		self.dividend_data = []

	def get_data(self):
		if self._does_path_exist():
			data = self._load_data_from_local()
		else:
			data = self._scrape_for_data()

		self.dividend_data = data

	def _load_data_from_local(self):
		rows = []
		with open(self._filename, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			for row in spamreader:
				rows.append([self._to_date(row[0]), float(row[1])])
		return np.array(rows)

	def _to_date(self, date):
		return datetime.datetime.strptime(date, '%m/%d/%Y').date()

	def _scrape_for_data(self):
		driver = webdriver.Safari()
		driver.get(self._url)
		_ = WebDriverWait(driver, self._page_load_timeout).until(EC.presence_of_element_located((By.ID, 'divvytable')))

		facts = driver.find_elements_by_id("divvytable")[0]

		csv_rows = []
		data_rows = []
		for i in facts.text.split("\n\n\n"):
			row = i.split("\n")
			if len(row) > 1 and row[0] != "Date":
				date = row[0]
				temp = date.split("/")
				if int(temp[2]) <= 21:  # 21 is liek the current year, problems for 100+ years
					temp[2] = "20" + temp[2]
				else:
					temp[2] = "19" + temp[2]
				date = "/".join(temp)

				amt = float(row[1])
				csv_rows.append([date, amt])
				data_rows.append([self._to_date(date), amt])

		with open(self._filename, "w+") as my_csv:
			csvWriter = csv.writer(my_csv, delimiter=',')
			csvWriter.writerows(csv_rows)

		return np.array(data_rows)

	def _does_path_exist(self):
		return path.exists(self._filename)

	def plot_dividends(self):
		x = np.flip(self.dividend_data.T[0])
		y = np.flip(self.dividend_data.T[1])

		plt.plot(x, y)
		plt.title("Dividend Payments for: %s" % self._ticker)
		plt.xlabel("Payment Date")
		plt.ylabel("Amount ($)")
		plt.show()


if __name__ == "__main__":
	ticker = "lb"
	scraper = Scraper(ticker)
	scraper.get_data()
	scraper.plot_dividends()
