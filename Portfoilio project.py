import pandas as pd
from decimal import Decimal

class User:
    def __init__(self, user_id):
        self.accounts = []
        self.user_id = user_id
    def add_account(self, account):
        self.accounts.append(account)

class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.owned_stocks = {}
    def buy_stock(self, stock, quantity):
        #if stock already owned
        if stock.ticker in self.owned_stocks.keys():
            #add quantity 
            self.owned_stocks[stock.ticker][1] += quantity
            self.owned_stocks[stock.ticker][2] += stock.price * quantity
            #add to total cost of stock owned
            
        else:
            self.owned_stocks[stock.ticker] = [stock, quantity, stock.price*quantity]
            #add to total cost of stock owned
        

    def sell_stock(self, stock_ticker, quantity):
        if stock_ticker in self.owned_stocks.keys() and self.owned_stocks[stock_ticker][1] >= quantity:
            self.owned_stocks[stock_ticker][1] = self.owned_stocks[stock_ticker][1] - quantity
            ##self.balance =+ self.owned_stocks[stock_ticker][0].price * quantity
            if self.owned_stocks[stock_ticker][1] == 0:
                self.owned_stocks.pop(stock_ticker)
        else:
            print("Stock or quantity not owned ")
        
    def __str__(self):
        print("Owned stocks: ")
        if (len(self.owned_stocks) > 0):
            for n in self.owned_stocks:
                print(self.owned_stocks[n][0].ticker, "|", self.owned_stocks[n][0].company_name, "|", "Quantity:", self.owned_stocks[n][1], "|", "Total Cost:", "$" + str(self.owned_stocks[n][2]))
            
class Stock:
    def __init__(self, ticker, price, company_name):
        self.company_name = company_name
        self.ticker = ticker
        self.price = price
    
class Hashtable:
    def __init__(self):
        self.table = {}
    
    def _hash(self, key):
        sumH = 0
        print(type(key))
        for x in key:
            sumH += ord(x)
        return sumH

    def set(self, key, value):
        hashed_key = self._hash(key)
        if hashed_key not in self.table:
            self.table[hashed_key] = []
        self.table[hashed_key] = value

    def get(self, key):
        hashed_key = self._hash(key)
        return self.table.get(hashed_key, None)
    
    def delete(self, key):
        hashed_key = self._hash(key)
        if hashed_key in self.table:
            del self.table[hashed_key]
     
portfolio1 = Account("ABCD", 300)
quinn = User("QL23")
quinn.add_account(portfolio1)


#Reading CSV data into a dictionary
#Turn this into hashmap later
#Automate downloading updated CSV hourly from https://www.nasdaq.com/market-activity/stocks/screener
stocks = pd.read_csv("stocks.csv")
tickers = list(stocks["Symbol"])
prices = list(stocks["Last Sale"])
company_name = list(stocks["Name"])

hashtbl = Hashtable()
for x in tickers:
    if type(x) == 'str':
        hashtbl.set(x, prices[tickers.index(x)])

#Interface    
num = 0
while num < 5:
    num = int(input("Enter 2 to buy a stock, 3 to sell a stock, 4 to display account details, 5 to open a new account, 6 to sign in to an account"))              
    if num == 2:
        ticker = input("Enter stock ticker to buy: ")
        #Searching through tickers list to find that stock index, faster with hashmap.
        stock_index = tickers.index(ticker)
        price = float(Decimal("".join(d for d in prices[stock_index] if d.isdigit() or d == '.')))
        stock = Stock(tickers[stock_index], price, company_name[stock_index])
        portfolio1.buy_stock(stock, int(input("Enter quantity: ")))
        
    if num == 3:
        portfolio1.sell_stock(input("Enter stock ticker to sell: "), int(input("Enter quantity to sell: ")))
    if num == 4:
        portfolio1.__str__()
    if num == 5:
        user_id = input("Enter user id: ")
        password = input("Enter password: ")
    if num == 6:
        user_id = input("Enter user id: ")
        password = input("Enter password: ")
