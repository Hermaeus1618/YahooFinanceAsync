# YAHOO FINANCE API ASYNCRONOUS
A Yahoo Finance API to fetch historical stock dataframe https://finance.yahoo.com.

Algorithm is made using `asyncio` to get most speed possible from server.
Very useful for bulk downloading in cases like backtesting strategy.

The function will return stock `[Quote, Dataframe]` as list cause quotes are also included in the response from server and contains live data about stock so not processing that will be a waste.
But do not worry you can easily seprate quotes and dataframe by a single liner list comprehension.

Number of concurrent requests is limited by `Semaphore`,
Values of `Semaphore` can be changed to as high as 148 (and higher) but higher values are susceptible to timeout errors (rarely on Yahoo).
This algorithm can also be used without `Semaphore` which means all requests at one, the reason for that Yahoo server can handle overloads quite efficiently.

I have included a test file for checking out this module, it fetches only stock listed on NSE under EQ series which are stored as `pandas.Series()` in __Symbol.xlsx__.
It will __NOT__ store or modify any data.
