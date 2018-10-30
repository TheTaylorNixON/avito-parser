import requests
from bs4 import BeautifulSoup


base_url = 'https://www.avito.ru/'
city = 'krasnodar?p='
page = '1'
query = '&q=айфон+8'
url = base_url + city + page + query        # https://www.avito.ru/krasnodar?p=1&q=айфон+8


def get_html(url: str):         # возвращает html код с запрашиваемой страницы    
    r = requests.get(url).text
    return r


def get_total_pages(html):      # возвращает номер последней страницы  -> int
    with open('test.txt', 'w') as qwe:
        print(html, file=qwe)
    soup = BeautifulSoup(html, "lxml")
    print(soup.find('div', class_='pagination-pages fDrSyailDdFM'))
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def main():                     # генерирует url для каждой страницы, передает его в get_page_data()
    total_pages = get_total_pages(get_html(url))
    for i in range (1, total_pages + 1):
        url_gen = base_url + city + str(i) + query
        html = get_html(url_gen)
        get_page_data(html)


def get_page_data(html):        # парсит страницу и возвращает словарь с данными
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ = 'js-catalog_after-ads').find_all('div', class_ = 'item_table')
    for ad in ads:
        try:
            title = ad.find('div', class_ = 'description').find('div', class_='item_table-header').find('h3').text.strip()
        except:
            title = 'Заголовок не задан'

        try:
            price = int(ad.find('div', class_ = 'description').find('div', class_='item_table-header').find('div',class_='about').text.strip().replace(' ', '').replace('₽', ''))
        except:
            price = 'Цена не указана'

        try:
            url = base_url + ad.find('div', class_ = 'description').find('div', class_='item_table-header').find('h3').find('a').get('href')
        except:
            url = ''
        
        try:
            time = ad.find('div', class_ = 'description').find('div', class_='data').find('div').text.strip()
        except:
            time = 'Время размещения неизвестно'
        
        try:
            fp = ad.find('div', class_ = 'description').find('div', class_='data').find_all('p')[0].text
            sp = ad.find('div', class_ = 'description').find('div', class_='data').find_all('p')[-1].text

            if fp != sp:
                place = sp            
            else:
                place = 'Район не указан'
        except:
            place = 'Район не указан'

        data = {'url': url,
                'title': title,
                'price': price,
                'place': place,
                'time': time}


if __name__ == '__main__':
    main()