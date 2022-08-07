from bs4 import BeautifulSoup
from lxml import etree
import requests
import pyodbc
import os

print('开始运行')

url_list = []

os.chdir('~') #更改目录

url_top250 = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

html_page = requests.get(url = url_top250).text
soup = BeautifulSoup(html_page, 'html.parser')

movie_td = soup.find_all('td', {'class': 'titleColumn'})
for line in movie_td:
    movie_a = line.find('a')['href']
    sep = '?'
    movie_a = movie_a.split(sep, 1)[0]
    url_list.append(movie_a)

with open("top250_url.txt","w+") as txtfile:
    for i in range(len(url_list)):
        txtfile.write(url_list[i] + '\n')
print('结束运行')
