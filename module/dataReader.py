import datetime
import os
import FinanceDataReader as fdr
import backtrader.feeds as btfeeds
import backtester

dtformat='%Y-%m-%d'

class customCSV(btfeeds.GenericCSVData):
    params=(
        ('dtformat', dtformat),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 6),
        ('openinterest', -1),
    )

class StockDataReader():
    stocks = []

    def __init__(self, stocks: list):
        self.stocks = stocks
        
    def getStockValueData(self, fromdate: str, enddate: str) -> list:
        customized = []
        for stock in self.stocks:
            df=fdr.DataReader(stock, fromdate, enddate)
            
            filename = stock + ".csv"
            filepath = os.path.join(backtester.modpath, "../data", filename)
            df.to_csv(filepath)
            
            customized.append(customCSV(dataname=filepath))
        return customized
