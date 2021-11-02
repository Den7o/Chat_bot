import requests
from bs4 import BeautifulSoup

URL = requests.get("https://24.kg/").text

def get_link(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find('div', {'class':'row lineNews'})
    item = items.find('div', {'class':'one'})
    link = "https://24.kg" + item.find('a').get('href')
    return link

def get_news(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.find('div', {'class':'cont'}).text
    print(text)

def main():
    link = get_link(URL)
    page = requests.get(link).text
    get_news(page)

if __name__ == "__main__":
    main()