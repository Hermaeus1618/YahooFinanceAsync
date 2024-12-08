import httpx
import asyncio
import numpy as np
import pandas as pd
import datetime as dt

def SyncYFCookie(HEADER) -> dict:
    URL=fr"https://fc.yahoo.com"

    RESULT=httpx.get(URL, headers=HEADER, follow_redirects=True)
    COOKIE={R[0]:R[1] for R in RESULT.cookies.items()}

    return COOKIE

async def AsyncYFStockQuoteGraphClosure(CLIENT, SEMAPHORE, TICKER, EXCHANGE, START, END, INTERVAL) -> list:
    URL=fr"https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}.{EXCHANGE}?TICKER={TICKER}.{EXCHANGE}&period1={round(START.timestamp())}&period2={round(END.timestamp())}&interval={INTERVAL}"
    
    async with SEMAPHORE:
        RESULT=await CLIENT.get(URL)

    INDEX=pd.Series([dt.datetime.fromtimestamp(t) for t in RESULT.json()["chart"]["result"][0]["timestamp"]], name="timeframe")
    DF=pd.DataFrame(RESULT.json()["chart"]["result"][0]["indicators"]["quote"][0], index=INDEX)[["open", "high", "low", "close", "volume"]]
    DF.columns=["into", "inth", "intl", "intc", "intv"]
    DF[['into', 'inth', 'intl', 'intc']]=DF[['into', 'inth', 'intl', 'intc']].infer_objects(copy=False).ffill().bfill()
    DF[['intv']]=DF[['intv']].infer_objects(copy=False).fillna(0)
    DF["intavg"]=DF[["into", "inth", "intl", "intc"]].transpose().mean()
    DF["intmflow"]=np.where(DF["intavg"]<=np.roll(DF["intavg"], 1), -1, 1)
    if(DF["into"].iloc[0]<DF["intc"].iloc[0]):
        DF.at[DF.index[0], "intmflow"]=1
    else:
        DF.at[DF.index[0], "intmflow"]=-1
    DF["intmflow"]=DF["intmflow"]*DF["intv"]*DF["intavg"]
    DF["name"]=TICKER
    DF=DF.reset_index()
    
    QUOTE=RESULT.json()["chart"]["result"][0]["meta"]

    print(TICKER)

    return [QUOTE, DF]

async def AsyncYFStockQuoteGraph(HEADER, TICKERS, EXCHANGE, START, END, INTERVAL) -> list[list]:
    CLIENT=httpx.AsyncClient(headers=HEADER)
    SEMAPHORE=asyncio.Semaphore(27)
    
    APOOL=[asyncio.create_task(AsyncYFStockQuoteGraphClosure(CLIENT, SEMAPHORE, TICKER, EXCHANGE, START, END, INTERVAL)) for TICKER in TICKERS]

    RESULT=await asyncio.gather(*APOOL)

    return RESULT

if __name__=="__main__":
    print("\x1b[31m\x1b[1mYou wouldn't do that, Specifically!\x1b[0m")