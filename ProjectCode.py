import requests
import time
import matplotlib.pyplot as plt
import telepot
# global variables
api_key = '2d6b4258-4c8d-462f-a284-cb0dd85f2cb6'
bot_token = '5650702897:AAGAyQIG4teWmgYcnAuJsotCcydep0B8sWk'
chat_id = '1700989901'
threshold = 17000
time_interval = 20  # in seconds


def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()
# extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']
    # fn to send_message through telegram


def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
# send the msg
    requests.get(url)
    # main fn


def main():
    price_list = []
# infinite loop
    while True:
        price = get_btc_price()
        price_list.append(price)
# if the price falls below threshold, send an immediate msg
        if price < threshold:
            send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: {price}')
# send last 6 btc price
        if len(price_list) == 3:
            send_message(chat_id=chat_id, msg=price_list)
            step = range(time_interval, 4*time_interval, time_interval)
            plt.plot(step, price_list)
            plt.xlabel("time interval in seconds")
            plt.ylabel("Bitcoin price variation")
            # plt.show()
            plt.savefig("graph.png")
            bot = telepot.Bot(bot_token)
            bot.sendPhoto(chat_id, photo=open('graph.png', 'rb'))

            # empty the price_list
            price_list = []
# fetch the price for every dash minutes
        time.sleep(time_interval)


# fancy way to activate the main() function
if __name__ == '__main__':
    main()