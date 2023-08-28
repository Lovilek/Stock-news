import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


end_point_stock = 'https://www.alphavantage.co/query/'
api_key_stock = 'P24P6WWRFNQYPFK2'
params_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_stock
}
r = requests.get(url=end_point_stock, params=params_stock)
data = r.json()
two_stocks = list(data["Time Series (Daily)"].items())[:2]
print(two_stocks)
first_day = float(two_stocks[0][1]["4. close"])
second_day = float(two_stocks[1][1]["4. close"])
one_percent = first_day / 100
difference = 100 - round(second_day / one_percent)
if difference < 0:
    emoji = "⬇"
else:
    emoji = "⬆"


end_point_news = 'https://newsapi.org/v2/everything/'
api_key_news = 'f53100aa20a545059d06282ec07f20cf'
params_news = {
    "apikey": api_key_news,
    "q": COMPANY_NAME,
    "sortBy": "popularity",
    "from": two_stocks[1][0],
    "to": two_stocks[0][0]
}
r = requests.get(url=end_point_news, params=params_news)
data = r.json()
three_news = data["articles"][:3]


account_sid = 'AC4c067a311cb216e274a864024eab570e'
auth_token = '1ee3076cf97c142875a4b5f9b9c5c50b'
if abs(difference) >= 5:
    client = Client(account_sid, auth_token)
    for it in three_news:
        message = client.messages.create(
            body=f'{STOCK}:{emoji}{abs(difference)}%\nHeadline: {it["title"]}\nBrief: {it["description"]}',
            from_='+18642522521',
            to='+77787329544'
        )
