import pandas as pd
import math
from decimal import Decimal

#Personal Paper Trader 
#Quinn Lindsey

class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.owned_stocks = {}
    def buy_stock(self, stock, quantity):
        #if stock already owned
        if stock.price * quantity > self.balance:
            print("Not enough funds")
            return
        if stock.ticker in self.owned_stocks.keys():
            #add quantity 
            self.owned_stocks[stock.ticker][1] += quantity
            self.owned_stocks[stock.ticker][2] += stock.price * quantity
            #add to total cost of stock owned
        else:
            self.owned_stocks[stock.ticker] = [stock, quantity, stock.price*quantity]
            #add to total cost of stock owned
        self.balance -= stock.price * quantity

    def sell_stock(self, stock_ticker, quantity):
        if stock_ticker in self.owned_stocks.keys() and self.owned_stocks[stock_ticker][1] >= quantity:
            self.owned_stocks[stock_ticker][1] = self.owned_stocks[stock_ticker][1] - quantity
            stock_sell_price = get_stock_price(self.owned_stocks[stock_ticker][0].ticker)
            self.balance += stock_sell_price * quantity
            self.owned_stocks[stock_ticker][2] = truncate(self.owned_stocks[stock_ticker][2] - stock_sell_price * quantity, 2)
            if self.owned_stocks[stock_ticker][1] == 0:
                self.owned_stocks.pop(stock_ticker)
        else:
            print("Stock or quantity not owned ")
    
    def __str__(self):
        print("Owned stocks: ")
        if (len(self.owned_stocks) > 0):
            print("Cash Balance: $" + str(self.balance))
            for n in self.owned_stocks:
                print("%10s" % self.owned_stocks[n][0].ticker, end=" | ")
                print("%48s" % self.owned_stocks[n][0].company_name, end=" | ")
                print("%5s" % (str(self.owned_stocks[n][1])), end=" | ")
                print("%10s" % "Total Cost: $" + str(self.owned_stocks[n][2]))

class Stock:
    def __init__(self, ticker, price, company_name):
        self.company_name = company_name
        self.ticker = ticker
        self.price = price

def get_stock_price(stock_ticker):
    index = tickers.index(stock_ticker)
    stock_price = float(Decimal("".join(d for d in prices[index] if d.isdigit() or d == '.')))
    return stock_price
    
def get_stock_info(ticker):
    index = tickers.index(ticker)
    return Stock(ticker, prices[index], company_name[index])

def truncate(number, digits) -> float:
    Decimals = len(str(number).split('.')[1]) 
    if Decimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
     
def get_account(id):
    line = None
    account = None
    with open("data.txt") as file:
        while True:
            line = file.readline()
            if id == line[:line.index(";")]:
                break
            if not(line):
                print("Account not found, try again.")
                exit()
            
        balance = line[line.index(";")+1:line.index("-")]
        stocks_line = line[line.index("-")+1:]
        account = Account(id, float(balance))
        while len(stocks_line) > 1:
            stock = stocks_line[:stocks_line.index(",")]
            ticker = stock[:stock.index(":")]
            quantity = int(stock[stock.index(":")+1:])
            stocks_line = stocks_line[len(stock)+1:]
            account.owned_stocks[ticker] = [get_stock_info(ticker), quantity, truncate(float(quantity) * get_stock_price(ticker), 2)]
    return account

def save_account(account):
    line = None
    lines = None
    data = ""

    data = str(account.account_id) + ";" + str(truncate(account.balance, 2)) + "-"
    for n in account.owned_stocks:
        data += account.owned_stocks[n][0].ticker + ":" + str(account.owned_stocks[n][1]) + ","
    
    #Find line that contains this account
    with open("data.txt", "r") as file:
        lines = file.readlines()
        counter = 0
        while True:
            line = lines[counter][:lines[counter].index(";")]
            if account.account_id in line:
                break
            counter += 1
        lines[counter] = data + "\n"
    
    #Write data
    with open("data.txt", "w") as file:
        for line in lines:
            file.write(line)

#Reading CSV data into a dictionary
#Eventually Automate downloading updated CSV hourly from https://www.nasdaq.com/market-activity/stocks/screener
stocks = pd.read_csv("stocks.csv")
tickers = list(stocks["Symbol"])
prices = list(stocks["Last Sale"])
company_name = list(stocks["Name"])


#Interface    
num = 0
#Enter ABC for test account
login_id = input("Enter account ID (use ABC for testing) to login: ")
account = get_account(login_id)

while num < 6:
    num = int(input("Enter 2 to buy a stock, 3 to sell a stock, 4 to display account details, 5 to exit and save: "))              
    if num == 2:
        ticker = input("Enter stock ticker to buy: ")
        stock_index = tickers.index(ticker)
        price = float(Decimal("".join(d for d in prices[stock_index] if d.isdigit() or d == '.')))
        stock = Stock(tickers[stock_index], price, company_name[stock_index])
        account.buy_stock(stock, int(input("Enter quantity: ")))
    if num == 3:
        account.sell_stock(input("Enter stock ticker to sell: "), int(input("Enter quantity to sell: ")))
    if num == 4:
        account.__str__()
    if num == 5:
        save_account(account)
        exit()
  
#Unit Tests
assert type(account.balance) is float
assert type(account.account_id) is str
assert len(stocks) > 0
assert len(tickers) > 0
assert len(prices) > 0
assert len(company_name) > 0
assert login_id == account.account_id
assert num < 6
assert get_stock_info("T").ticker == "T"
assert get_stock_price("T") == get_stock_info("T").price