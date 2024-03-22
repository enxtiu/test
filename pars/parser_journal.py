from requests import Session
from bs4 import BeautifulSoup

def pars_homework_j(name: str, password: str):

    global headers, url_login, url_login_mark, url_login_homework

    def soup(result):
        return BeautifulSoup(result.text, 'lxml')


    def get_url():
        url_jornal = soup(response_journal).find('ul', class_='education-menu').find_all('li')

        for i in url_jornal:
            url_mark = 'https://cabinet.ruobr.ru/login/?next=' + i.find('a').get('href')
            yield url_mark


    session = Session()

    response_login = session.get(url_login, headers=headers)

    token = soup(response_login).find('form', class_='ui form').find('input').get('value')

    data = {
        'csrfmiddlewaretoken': token,
        'next': '/',
        'username': name,
        'password': password
    }

    response_journal = session.post(url_login, headers=headers, data=data, allow_redirects=True)

    for url in get_url():
        if url == url_login_homework:
            response_homework = session.post(url,  headers=headers,  data=data,  allow_redirects=True)
            tern_data_ivent_all = soup(response_homework).find('table', class_='homework_list').find('tbody').find_all('td')
            stroka = ''
            for index in range(0, len(tern_data_ivent_all)):
                tern_data_ivent = tern_data_ivent_all[index].text.strip().replace('\n', '')
                stroka += '\n' + tern_data_ivent
            return stroka


def pars_number_j(name: str, password: str):

    global headers, url_login, url_login_mark, url_login_homework

    def soup(result):
        return BeautifulSoup(result.text, 'lxml')


    def get_url():
        url_jornal = soup(response_journal).find('ul', class_='education-menu').find_all('li')

        for i in url_jornal:
            url_mark = 'https://cabinet.ruobr.ru/login/?next=' + i.find('a').get('href')
            yield url_mark


    session = Session()

    response_login = session.get(url_login, headers=headers)

    token = soup(response_login).find('form', class_='ui form').find('input').get('value')

    data = {
        'csrfmiddlewaretoken': token,
        'next': '/',
        'username': name,
        'password': password
    }

    response_journal = session.post(url_login, headers=headers, data=data, allow_redirects=True)

    for url in get_url():
        if url == url_login_mark:
            response_mark = session.post(url, headers=headers,  data=data,  allow_redirects=True)
            mark = soup(response_mark).find('table', class_='hide').find_all('tr')
            stroka = ''
            for index in range(0, len(mark)):
                b = len(mark[index].text.strip().replace('\n', ' '))
                c = 0
                d = 0
                while True:
                    if mark[index].text.strip().replace('\n', ' ')[b::-1][c] in '0123456789.':
                        c += 1
                    else:
                        break
                while True:
                    if mark[index].text.strip().replace('\n', ' ')[:b-c:][::-1][d] in ' ':
                        d += 1
                    else:
                        break

                item_mark = mark[index].text.strip().replace('\n', ' ')[:b - c - d]
                item_mark_1 = mark[index].text.strip().replace('\n', ' ')[b - c:]
                if index == 0:
                    stroka += item_mark + ':' + '\n\n'
                else:
                    stroka += '\n' + item_mark + ':' + '\n' + 'Средний бал -> ' + item_mark_1 +';' + '\n'
            return stroka




headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'csrftoken=MideYUS5jrV66ykd0bdIR4nXlgKERGiN; _ym_uid=16764128791015051556; _ym_d=1697503088',
    'Origin': 'https://cabinet.ruobr.ru',
    'Referer': 'https://cabinet.ruobr.ru/login/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

url_login_mark = 'https://cabinet.ruobr.ru/login/?next=/child/studies/mark_table/'
url_login_homework = 'https://cabinet.ruobr.ru/login/?next=/child/studies/homework/'
url_login = 'https://cabinet.ruobr.ru/login/'
