import pandas as pd
from decimal import Decimal

class User:
    def __init__(self, userID):
        self.accounts = []
        self.userID = userID
    def addAccount(self, account):
        self.accounts.append(account)

class Account:
    def __init__(self, accountID, balance):
        self.accountID = accountID
        self.balance = balance
        self.ownedstocks = {}
    def buyStock(self, stock, quantity):
        #if stock already owned
        if stock.ticker in self.ownedstocks.keys():
            #add quantity 
            self.ownedstocks[stock.ticker][1] += quantity
            self.ownedstocks[stock.ticker][2] += stock.price * quantity
            #add to total cost of stock owned
            
        else:
            self.ownedstocks[stock.ticker] = [stock, quantity, stock.price*quantity]
            #add to total cost of stock owned
        

    def sellStock(self, stock_ticker, quantity):
        if stock_ticker in self.ownedstocks.keys() and self.ownedstocks[stock_ticker][1] >= quantity:
            self.ownedstocks[stock_ticker][1] = self.ownedstocks[stock_ticker][1] - quantity
            ##self.balance =+ self.ownedstocks[stock_ticker][0].price * quantity
            if self.ownedstocks[stock_ticker][1] == 0:
                self.ownedstocks.pop(stock_ticker)
        else:
            print("Stock or quantity not owned ")
        
    def __str__(self):
        print("Owned stocks: ")
        if (len(self.ownedstocks) > 0):
            for n in self.ownedstocks:
                print(self.ownedstocks[n][0].ticker, "|", self.ownedstocks[n][0].companyName, "|", "Quantity:", self.ownedstocks[n][1], "|", "Total Cost:", "$" + str(self.ownedstocks[n][2]))
            
class Stock:
    def __init__(self, ticker, price, companyName):
        self.companyName = companyName
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
quinn.addAccount(portfolio1)


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



##Interface    
num = 0
while num < 5:
    num = int(input("Enter 2 to buy a stock, Enter 3 to sell a stock, Enter 4 to display account details, Enter 5 to exit: "))              
    if num == 2:
        ticker = input("Enter stock ticker to buy: ")
        #Searching through tickers list to find that stock index, faster with hashmap.
        stockIndex = tickers.index(ticker)
        price = float(Decimal("".join(d for d in prices[stockIndex] if d.isdigit() or d == '.')))
        stock = Stock(tickers[stockIndex], price, company_name[stockIndex])
        portfolio1.buyStock(stock, int(input("Enter quantity: ")))
        
    if num == 3:
        portfolio1.sellStock(input("Enter stock ticker to sell: "), int(input("Enter quantity to sell: ")))
    if num == 4:
        portfolio1.__str__()
