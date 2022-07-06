from bs4 import BeautifulSoup
import requests
import time
import smtplib

# prices[i] - > Rate
# i -> Name

def price_decrease_check(old_prices,new_prices):
    for i in (old_prices):
        for j in (new_prices):
            if i == j:
                if new_prices[j] < (old_prices[i] * 0.9):    # If there is 10% DROP in price, email is sent
                    send_email(i,old_prices[i],new_prices[i])

def send_email(coinname, oldvalue,newvalue):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    message = f"The coin {coinname} has reduced from ${oldvalue} to ${newvalue}"
    s.login("SENDER EMAIL", "SENDER PASSWORD")  # Allow Less secure App access in senders google account
    s.sendmail("SENDER EMAIL", receiver_email, message)
    s.quit()

def get_price():
    url = "https://coinmarketcap.com/"
    result=requests.get(url).text
    doc = BeautifulSoup(result,"html.parser")

    tbody = doc.tbody
    trs = tbody.contents

    prices ={}

    for tr in trs[:10]:
        name, price = tr.contents[2:4]
        fixed_name = name.p.string
        fixed_price = price.a.string

        prices[fixed_name] = float(fixed_price.replace(',','').replace('$',''))
    return (prices)

receiver_email=input("Please Enter the email for notifications: ")
count = 1 
while True:
    if count<=1:
            old_prices = get_price()
    if count>1:
        new_prices = get_price()
        flag = price_decrease_check(old_prices,new_prices)
        old_prices = new_prices
    time.sleep(43200) # No. of seconds (43000s - 12 hours)
    count+=1