#ts217

import yfinance as yf
from fastapi import FastAPI

class Stock:

    def __init__(self,ticker:str):
        self._ticker = ticker.upper()+".SA"
        self._stock = yf.Ticker(self._ticker)

    def __set_Basic_Information(self)->dict:
        basicData ={"Symbol":self._stock.info.get("symbol"),"Sector":self._stock.info.get("sector"),"industry":self._stock.info.get("industry")}
        return basicData

    def get_Basic_information_stock_Json(self)->str:
        return self.__set_Basic_Information()
    
    def __set_Stock_Current_Price(self)->dict:
        currentPrice = {"current price":self._stock.info.get("currentPrice")}
        return currentPrice
    
    def get_Stock_Current_Price_json(self)->str:
        return self.__set_Stock_Current_Price()
    
    def get_history_month(self) -> list[float]:
       return self._stock.history(period="max")["Close"].tolist()
    
    def get_history(self) -> dict:
       df = self._stock.history(period="max")
       df = df.reset_index()[["Date","Close"]]
       return df.to_dict(orient="records")


    
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

@app.get("/maxHistory")
def mouth(stock:str):
    return (Stock(stock).get_history())