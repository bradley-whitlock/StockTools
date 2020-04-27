# Inflation Data is currently only from Canada

import numpy as np 
import json
from requests import post
from datetime import datetime

class InflationUtils:
	def __init__(self, start_date, end_date = str(datetime.date(datetime.now()))):
		self._start_date = start_date
		self._end_date = end_date
		self.data = self.get_inflation_series()

	def get_inflation_series(self):
		url = 'https://www150.statcan.gc.ca/t1/wds/rest/getBulkVectorDataByRange'
		
		start = self._start_date + 'T00:00'
		end = self._end_date + 'T00:00'
		params = {
			"vectorIds": ["41690973","1"],
			"startDataPointReleaseDate": start,
			"endDataPointReleaseDate": end 
			}

		r = post(url, json = params)
		json_response = r.json()

		points = json_response[-1]["object"]['vectorDataPoint']

		data = []
		for point in points:
			data.append([point['refPer'],point['value']])

		return np.array(data).T

	def adjust_stock_for_inflation(self):
		pass

	def adjust_dividend_for_inflation(self):
		pass

if __name__ == '__main__':
	start_date = '2020-01-01'
	end_date = '2020-04-30'

	inflation = InflationUtils(start_date)
	print(inflation.data)
