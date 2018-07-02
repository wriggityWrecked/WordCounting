"""
http://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-morningstar
"""
from datetime import timedelta, datetime

import pandas_datareader.data as web


def get_stock_price(stock_initials, start_date, end_date):
    """

    :param stock_initials:
    :param start_date:
    :param end_date:
    :return:
    """
    return web.DataReader(stock_initials, 'morningstar', start_date, end_date)['Close']

if __name__ == "__main__":

    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    last_week = (now - timedelta(days=8)).strftime("%Y-%m-%d")
    df = get_stock_price('TSLA', last_week, tomorrow)
