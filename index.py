import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


def get_content(page):
    url = 'https://www.js100.com/en/site/home/search_advance/' + str(page)
    myobj = {'search_result_input': 'อุบัติเหตุ', 'newstype': 'trafic'}
    web_data = requests.post(url, myobj)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'html.parser')
    find_word = soup.find('ul', id='search_result_list')
    data = find_word.find_all('li')

    ls = []
    for row in data:
        ls_element = []
        ls_element.append(row.find('h4').text)
        ls_element.append(row.find('p').text)
        ls += [ls_element]

    df = pd.DataFrame(ls)
    df.columns = ['date', 'description']

    return df


df_all = pd.DataFrame()
i = 0
while(i <= 6740):
    try:
        if(i == 0):
            df = get_content('')
            df_all = pd.concat([df_all, df], axis=0, sort=False)
        else:
            df = get_content(i)
            df_all = pd.concat([df_all, df], axis=0, sort=False)

        print(f'Done getting data from page {i}')
        i += 20
    except:
        print(f'Cannot get data from page {i}')

print(df_all)
df_all.to_excel('accident_data.xlsx', index=False)
