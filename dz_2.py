import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

url = 'https://irkutsk.hh.ru/search/vacancy'
# https://irkutsk.hh.ru/search/vacancy?text=Data+science&from=suggest_post&salary=&ored_clusters=true&enable_snippets=true
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

vacancy_list = []

params = {
    'page': '1',
    'text': 'Data science',
    'from': 'suggest_post',
    'salary': '',
    'ored_clusters': 'true',
    'enable_snippets': 'true'
}


while True:
    session = requests.Session()
    response = session.get(url=url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancy = dom.find_all('div', {'class': 'serp-item__title'})
    if len (vacancy) == 0:
        break
    params ['page'] +=1
    for item in vacancy:
        vacancy_data = {}
        block_a = item.find('a', {'class': 'post-item__title'})
        href = block_a.get('href')
        name = block_a.text
        compensation = item.find('span', {'class': 'bloko-header-section-3'})
        if compensation:
            compensation = compensation.text
        vacancy_data['name'] = name
        vacancy_data['href'] = href
        vacancy_data['website'] = 'hh.ru'
        dict_1 = {}
        item_1 = (str(compensation)).replace('\u202f', '')
        if item_1[0].isdigit():
            re_min_max = re.compile(r'\d+')
            re_currency= re.compile(r'\w+')
            minimum = re_min_max.findall(item_1)[0]
            maximum = re_min_max.findall(item_1)[1]
            currency = re_currency.findall(item_1)[-1]
            dict_1['minimum'] = int(minimum)
            dict_1['maximum'] = int(maximum)
            dict_1['currency'] = currency
            vacancy_data['compensation'] = dict_1
        if item_1[0] == 'о':
            re_min_max = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            minimum = re_min_max.findall(item_1)[0]
            currency = re_currency.findall(item_1)[-1]
            dict_1['minimum'] = int (minimum)
            dict_1['currency'] = currency
            vacancy_data['compensation'] = dict_1
        if item_1[0] == 'д':
            re_min_max = re.compile(r'\d+')
            re_currency= re.compile(r'\w+')
            maximum = re_min_max.findall(item_1)[0]
            currency = re_currency.findall(item_1)[-1]
            dict_1['maximum'] = int (maximum)
            dict_1['currency'] = currency
            vacancy_data['compensation'] = dict_1
        if item_1 == 'None':
            vacancy_data['compensation'] = None
        vacancy_list.append(vacancy_data)

print(len(vacancy_list))
print(vacancy_list)


