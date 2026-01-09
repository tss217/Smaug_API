#ts217

import yfinance as yf
from fastapi import FastAPI

dat = yf.Ticker("BBAS3.SA")


class Stock:
    def __init__(self,ticker:str):
        self._ticker = ticker
        self._stock = yf.Ticker(ticker)

    def __set_Basic_Information(self)->dict:
        basicData ={"Symbol":self._stock.info.get("symbol"),"Sector":self._stock.info.get("sector"),"industry":self._stock.info.get("industry")}
        return basicData

    def get_Basic_information_stock_Json(self)->dict:
        return self.__set_Basic_Information()
    
    def __set_Stock_Current_Price(self)->dict:
        currentPrice = {"current price":self._stock.info.get("currentPrice")}
        return currentPrice
    
    def get_Stock_Current_Price_json(self)->str:
        return self.__set_Stock_Current_Price()

    
app = FastAPI(title="Smaug")

@app.get("/")
def root():
    return {"status":"ok"}
    
@app.get("/stock")
def stock(stock:str):
    st  = Stock(stock)
    return st.get_Stock_Current_Price_json()

@app.get("/stockinfo")
def info(stock:str):
    st = Stock(stock)
    return st.get_Basic_information_stock_Json()