import numpy as np
from os import path
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from common import *


class CanadianDividendUtils:
	def __init__(self, ticker, start_date):
		self._ticker = ticker
		self._start_date = to_date_object(start_date, format="%Y-%m-%d")

		self._page_load_timeout = 10
		self._data_dir = "data"

		# For the dividend data
		self._base_url = "https://www.canadastockchannel.com/profile/?symbol="
		self._url = "%s%s" % (self._base_url, self._ticker)
		self._dividend_filename = "%s_dividends.csv" % self._ticker
		self._dividend_filename_with_dir = "%s/%s" % (self._data_dir, self._dividend_filename)

		self.data = self.load_data()

	def _data_has_been_scraped(self):
		return path.exists(self._dividend_filename_with_dir)

	def _load_data_from_local(self):
		rows = []
		with open(self._dividend_filename_with_dir, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			for row in spamreader:
				rows.append([to_date_object(row[0], format="%m/%d/%Y"), float(row[1])])
		return np.array(rows).T

	def _scrape_for_dividend_data(self):
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
				if int(temp[2]) <= 21:  # 21 is like the current year, problems for 100+ years
					temp[2] = "20" + temp[2]
				else:
					temp[2] = "19" + temp[2]
				date = "/".join(temp)

				amt = float(row[1])
				csv_rows.append([date, amt])
				data_rows.append([to_date_object(date, format="%m/%d/%Y"), amt])

		# Want the data in ascending order for plotting, might need to do for data_rows too??
		csv_rows.reverse()
		data_rows.reverse()

		if len(data_rows) > 0:
			with open(self._dividend_filename_with_dir, "w+") as my_csv:
				csvWriter = csv.writer(my_csv, delimiter=',')
				csvWriter.writerows(csv_rows)

		return np.array(data_rows).T

	def load_data(self):
		if self._data_has_been_scraped():
			data = self._load_data_from_local()
		else:
			data = self._scrape_for_dividend_data()

		# No dividend data is possible
		if data.size == 0:
			return None

		if self._start_date:
			valid_indicies = np.where(data[0] > self._start_date)
			data = data.T[valid_indicies].T

		return data

	def latest(self):
		return self.data[1][-1]
