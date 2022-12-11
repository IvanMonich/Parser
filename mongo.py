import pymongo
import scrapper

client = pymongo.MongoClient('mongodb+srv://Ivan:89182754291IM@cluster0.jwbit.mongodb.net/?retryWrites=true&w=majority')

db = client['myFirstDatabase']

clients_collection = db['clients']
news_collection = db['quotes']


def add_client(client_id):
    clients_collection.insert_one({"client_id": client_id, "is_mailing": True})

    return 1


def get_active_clients():
    active_clients = clients_collection.find({"is_mailing": True})

    return list(active_clients)


def get_quotes():
    quotes = news_collection.find({})

    return list(quotes)


def add_news(text, author, author_href, tags):
    news_collection.insert_one({"text": text, "author": author, "author_href": author_href, "tags": tags})

    return 1


def on_mailing(client_id):
    active_client = clients_collection.find_one({"client_id": client_id})
    if active_client is None:
        add_client(client_id)
    clients_collection.replace_one({"client_id": client_id}, {"client_id": client_id, "is_mailing": True})

    return "Теперь вы подписаны на рассылку"


def off_mailing(client_id):
    active_client = clients_collection.find({"client_id": client_id})
    if not active_client:
        add_client(client_id)
    clients_collection.replace_one({"client_id": client_id}, {"client_id": client_id, "is_mailing": False})

    return "Теперь вы отписаны от рассылки"


def refresh():
    quotes = scrapper.parse_start()
    news_collection.delete_many({})
    for i in range(len(quotes)):
        news_collection.insert_one(quotes[i])

    return 1

