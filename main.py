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
    
    def get_history_month(self) -> list[float]:
       df = self._stock.history(period="max")
       df = df.reset_index()[["Date","Close"]]
       return df.to_dict(orient="records")

class StatisticStock(Stock):
    def __init__(self, ticker):
        super().__init__(ticker)

        self._PL = None
        self._DY = None
        self._ROE = None
        self._margemBruta = None
        self._dividaLiquidaEbitda = None 

        self._set_PL
        self._set_DY
        self._set_ROE
        self._set_divida_Liquida_eitda

    @property
    def _set_PL(self)->None:
        self._PL = self.get_key_information("trailingPE")

    @property
    def _set_DY(self)->None:
        self._DY = self.get_key_information("dividendYield")

    @property
    def _set_ROE(self):
        self._ROE = self.get_key_information("returnOnEquity")*100

    @property
    def _set_margem_bruta (self):
        self._margemBruta = self.get_key_information("grossMargins")*100

    @property
    def _set_debt(self):
        return self.get_key_information("totalDebt")
    
    @property
    def _set_total_cash(self):
        return self.get_key_information("totalCash")
    
    @property
    def _set_ebitda(self):
        return self.get_key_information("ebitda")

    @property
    def _set_divida_Liquida_eitda(self):
        self._dividaLiquidaEbitda = (self._set_debt - self._set_total_cash) / self._set_ebitda
    

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

@app.get("/mouth")
def mouth(stock:str):
    return (Stock(stock).get_history_month())

@app.get("/test")
def testUrl(stock:str):
    return Stock(stock).set_key_information("dividendYield")