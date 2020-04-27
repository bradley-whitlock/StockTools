import datetime


def to_date_object(date, format):
	return datetime.datetime.strptime(date, format).date()
