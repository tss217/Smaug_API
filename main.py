#ts217

import yfinance as yf
from fastapi import FastAPI

class Stock:

    def __init__(self,ticker:str):
        self._ticker = ticker.upper()+".SA"
        self._stock = yf.Ticker(self._ticker)

    
    def get_key_information(self,keys:list[str]):
        info = self._stock.info
        return {k: info.get(k) for k in keys}

    def __set_Basic_Information(self)->dict:
        #basicData ={"Symbol":self._stock.info.get("symbol"),"Sector":self._stock.info.get("sector"),"industry":self._stock.info.get("industry")}
        return self.get_key_information(["symbol","sector","industry","dividendYield","operatingMargins","trailingEps","trailingPE","forwardPE"])

    def get_Basic_information_stock_Json(self)->str:
        return self.__set_Basic_Information()
    
    def __set_Stock_Current_Price(self)->dict:
        currentPrice = {"current price":self._stock.info.get("currentPrice")}
        return currentPrice
    
    def get_Stock_Current_Price_json(self)->str:
        return self.__set_Stock_Current_Price()

class HistoryStock(Stock):
    def __init__(self, ticker,period):
        super().__init__(ticker)

        self._period = period
        self._VALID_PERIOD = {"1d", "5d", "1mo", "3mo", "6mo","1y", "2y", "5y", "10y", "ytd", "max"}

    def get_period(self):
        if self._period not in self._VALID_PERIOD:
            return "periodo invalido"
        return self._period

    def get_history(self):
        df = self._stock.history(period=self.get_period())
        df = df.reset_index()[["Date","Close"]]
        return df.to_dict(orient="records")
    
class Currency():
    pass


app = FastAPI(title="Smaug")

@app.get("/")
def root():
    return {"status":"ok"}
    
@app.get("/stock")
def stock(stock:str):
   return Stock(stock).get_Stock_Current_Price_json()

@app.get("/infostock")
def info(stock:str):
        return Stock(stock).get_Basic_information_stock_Json()

@app.get("/history/{stock}/{period}")
def mouth(stock:str,period:str):
    his = HistoryStock(stock,period)
    return his.get_history()
