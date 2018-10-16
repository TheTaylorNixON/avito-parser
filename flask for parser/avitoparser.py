import requests     # что бы работать с интернетом
from bs4 import BeautifulSoup
# import самописного класса для работы с БД
from mysql_wrapper import UseDataBase


base_url = 'https://www.avito.ru/'
page = '?p='
page_num = '1'
query = '&q='

# sql запрос
_SQL = ''' insert into parse
        (title, price, time, place, url) 
        values
        (%s, %s, %s, %s, %s) '''

parser_db = UseDataBase()        


def get_url(city, search):
    url = base_url + city + page + page_num + query + search
    return url


def get_html(url): # возвращает html код с запрашиваемой страницы    
    r = requests.get(url).text
    return r


def get_total_pages(html): # возвращает номер последней страницы  -> int
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def main_parsing(city_input, search_input): # генерирует url для каждой страницы, передает его в get_page_data()
    city = city_input.replace(' ', '_').lower()
    search = search_input.replace(' ', '+')  
    url = get_url(city, search)
    total_pages = get_total_pages(get_html(url))

    # подключени к БД с параметрами dbconfig
    parser_db.create_connection()
    parser_db.query_insert('truncate table parse')

    # парсинг
    for i in range (1, total_pages + 1):
        url_gen = base_url + city + page + str(i) + query + search
        html = get_html(url_gen)
        get_page_data(html)

    # отключение от БД
    parser_db.close()

    return True


def get_page_data(html): # парсит страницу и импортирует данные в БД
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
        
        try:
            url = base_url + ad.find('div', class_ = 'description').find('div', class_='item_table-header').find('h3').find('a').get('href')
        except:
            url = 'Невозможно прочитать URL'  
        
        # импорт в БД
        parser_db.query_insert(_SQL, (title, price, time, place, url))