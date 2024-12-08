import asyncio
import pandas as pd
import datetime as dt

import yfcore as YFCore

HEADER={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
}

TICKERS=pd.read_excel("Symbol.xlsx")["SYMBOL"].to_list()
END=dt.datetime.today()
START=END-dt.timedelta(days=360*2)
EXCHANGE="NS"
INTERVAL="1d"

RESULT=asyncio.run(YFCore.AsyncYFStockQuoteGraph(HEADER, TICKERS, EXCHANGE, START, END, INTERVAL))

