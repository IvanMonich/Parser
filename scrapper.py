import requests
from bs4 import BeautifulSoup


def get_pages_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        is_quotes = soup.find_all("div", class_="row")[-1].find("div", class_="col-md-8").find("nav").find("ul", class_="pager").find("li", class_="next").find("a")['href']
    except:
        return int(url.replace('https://quotes.toscrape.com/page/', '')[:-1])

    if is_quotes:
        next_page = 'https://quotes.toscrape.com' + str(is_quotes)
        return get_pages_count(next_page)
    else:
        return int(url.replace('https://quotes.toscrape.com/page/', '')[:-1])


def parse_all(pages_count):
    result = []

    for i in range(1, pages_count + 1, 1):
        response = requests.get(f'https://quotes.toscrape.com/page/{i}/')
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all("div", class_="row")[-1].find("div", class_="col-md-8").find_all("div", class_="quote")

        for j in range(len(quotes)):
            text = quotes[j].find("span", class_="text").text
            author = quotes[j].find("small", class_="author").text
            author_href = "https://quotes.toscrape.com/" + str(quotes[j].find("a")['href'])
            tags = quotes[j].find("div", class_="tags").find_all("a")
            for k in range(len(tags)):
                tags[k] = tags[k].text
            result.append({"text": text, "author": author, "author_href": author_href, "tags": tags})

    return result


def parse_start():
    pages_count = get_pages_count('https://quotes.toscrape.com/')
    return parse_all(pages_count)
