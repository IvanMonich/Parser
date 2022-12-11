import threading
from random import randint
import time
import schedule
import telebot
import mongo

bot = telebot.TeleBot('5128690122:AAHzK2n2gJDVE14VRL8NXViJJdIm7p5bzGI')


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "/commands - информация о командах")
    elif message.text == '/on_mailing':
        text = mongo.on_mailing(message.from_user.id)
        bot.send_message(message.from_user.id, f"*{text}*\n/commands - информация о командах", parse_mode="Markdown")
    elif message.text == '/off_mailing':
        text = mongo.off_mailing(message.from_user.id)
        bot.send_message(message.from_user.id, f"*{text}*\n/commands - информация о командах", parse_mode="Markdown")
    elif message.text == '/quotes_all':
        quotes = mongo.get_quotes()
        for quote in quotes:
            bot.send_message(message.from_user.id,
                             f'_{quote["text"]}_\n\n*Author: *{quote["author"]}, {quote["author_href"]}\n\n*Tags: *{quote["tags"]}',
                             parse_mode="Markdown")
    elif message.text == '/quotes_random':
        quotes = mongo.get_quotes()
        quote = quotes[randint(0, len(quotes) - 1)]
        bot.send_message(message.from_user.id,
                         f'_{quote["text"]}_\n\n*Author: *{quote["author"]}, {quote["author_href"]}\n\n*Tags: *{quote["tags"] or "None"}',
                         parse_mode="Markdown")
    elif message.text == '/commands':
        bot.send_message(message.from_user.id, '/on_mailing - подписаться на рассылку\n'
                                               '/off_mailing - отписаться от рассылки\n'
                                               '/quotes_all - все цитаты\n'
                                               '/quotes_random - случайная цитата')
    else:
        bot.send_message(message.from_user.id, 'Напиши /commands')


def broadcast_random():
    quotes = mongo.get_quotes()
    clients = mongo.get_active_clients()
    quote = quotes[randint(0, len(quotes) - 1)]
    for active_client in clients:
        bot.send_message(active_client['client_id'],
                         f'_{quote["text"]}_\n\n*Author: *{quote["author"]}, {quote["author_href"]}\n\n*Tags: *{quote["tags"] or "None"}',
                         parse_mode="Markdown")
    return 1


def is_time_to_send():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every(10).seconds.do(broadcast_random)
schedule.every(30).minutes.do(mongo.refresh)


receive_thread = threading.Thread(target=is_time_to_send)
receive_thread.start()
bot.polling(none_stop=True, interval=0)
