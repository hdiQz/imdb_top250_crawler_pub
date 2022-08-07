from bs4 import BeautifulSoup
import requests
import pyodbc
import os

print('开始运行')
os.chdir('~') #更改目录
column_name = ['tt', 'title', 'year', 'movie_ratings', 'runtimeStr', 'imdb_rating', 'total_rating_amount', 'genres', 'plot', 'user_review_amount', 'critic_review_amount', 'metascore', 
                'budget', 'gross_US_and_Canada', 'opening_weekend_US_and_Canada', 'opening_weekend_US_and_Canada_date', 'gross_worldwide']

txtfile = open("top250_url.txt",'r')
txtfile_content = txtfile.readlines()
for i in range(0, 250):
    title_url = txtfile_content[i].replace('\n', '')
    #print(title_url)
    tt = title_url.replace('/', '').replace('title', '').replace('tt', '')
    #txt读取某一行
    initial_url = 'https://www.imdb.com'
    movie_url = initial_url + title_url
    #print(movie_url)

    html_page = requests.get(url = movie_url, proxies = None).text
    soup = BeautifulSoup(html_page, 'html.parser')
    #print(soup)

    #名称
    title = soup.find('h1', {'data-testid': 'hero-title-block__title'}).get_text().strip()
    #print(title)

    #年份、评级、时长
    meta_data_1 = soup.find_all('a', {'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color TitleBlockMetaData__StyledTextLink-sc-12ein40-1 rgaOW'})
    try:
        year = meta_data_1[0].get_text().strip() #年份 error
        movie_ratings = meta_data_1[1].get_text().strip() #评级
        runtimeStr = soup.find_all('li', {'class': 'ipc-inline-list__item'})[2].get_text().strip() #时长（小时）
        #print(year, movie_ratings, runtimeStr)
    except IndexError:
        year = meta_data_1[0].get_text().strip() #年份
        movie_ratings = None
        runtimeStr = soup.find_all('li', {'class': 'ipc-inline-list__item'})[1].get_text().strip() #时长（小时）
        if runtimeStr == 'Cast & crew':
            runtimeStr = None
        #print(year, movie_ratings, runtimeStr)
    except IndexError:
        year = meta_data_1[0].get_text().strip() #年份
        movie_ratings = None
        runtimeStr = None
        #print(year, movie_ratings, runtimeStr)

    #imdb评分
    try:
        imdb_rating = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'}).get_text().strip().replace('/10', '')
        imdb_rating = float(imdb_rating)
        #print(imdb_rating)
    except:
        imdb_rating = None
        #print(imdb_rating)

    #评分数量
    try:
        total_rating_amount = soup.find('div', {'class': 'AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ'}).get_text().strip()
        #print(total_rating_amount)
    except:
        total_rating_amount = None
        #print(total_rating_amount)

    #趋势分
    #trending_score = soup.find('div', {'class': 'TrendingButton__TrendingScore-bb3vt8-1 gfstID'}).get_text().strip() #趋势分数（实时），没啥必要

    #艺术风格
    try:
        genres = soup.find('div', {'data-testid': 'genres'}).get_text(',').strip()
        #print(genres)
    except:
        genres = None
        #print(genres)

    #情节概括
    try:
        plot = soup.find('span', {'data-testid': 'plot-xl'}).get_text().strip()
        #print(plot)
    except:
        plot = None
        #print(plot)

    #用户影评数量、批评家影评数量、媒体综合评分
    try:
        meta_data_2 = soup.find_all('span', {'class': 'score'})
        user_review_amount = meta_data_2[0].get_text().strip() #用户影评数量
        critic_review_amount = meta_data_2[1].get_text().strip() #批评家影评数量
        metascore = soup.find('span', {'class': 'score-meta'}).get_text().strip() #媒体综合评分
        #print(user_review_amount, critic_review_amount, metascore)
    except AttributeError:
        meta_data_2 = soup.find_all('span', {'class': 'score'})
        user_review_amount = meta_data_2[0].get_text().strip()
        critic_review_amount = meta_data_2[1].get_text().strip()
        metascore = None
        #print(user_review_amount, critic_review_amount, metascore)
    except AttributeError:
        user_review_amount = None
        critic_review_amount = None
        metascore = None
        #print(user_review_amount, critic_review_amount, metascore)

    #票房：预算、北美总票房、首映周末票房纪录（北美）、首映周末票房纪录（北美）日期、全球总票房
    try:
        budget = soup.find('li', {'data-testid': 'title-boxoffice-budget'}).get_text().strip().replace('Budget', '') #预算
        #print(budget)
    except:
        budget = None
        #print(budget)
    try:
        gross_US_and_Canada = soup.find('li', {'data-testid': 'title-boxoffice-grossdomestic'}).get_text().strip().replace('Gross US & Canada', '') #北美总票房
        #print(gross_US_and_Canada)
    except:
        gross_US_and_Canada = None
        #print(gross_US_and_Canada)
    try:
        opening_weekend_US_and_Canada_li = soup.find('li', {'data-testid': 'title-boxoffice-openingweekenddomestic'}).get_text('/').strip().replace('Opening weekend US & Canada/', '')
        #print(opening_weekend_US_and_Canada_li)
        sep = '/'
        opening_weekend_US_and_Canada = opening_weekend_US_and_Canada_li.split(sep, 1)[0] #首映周末票房纪录（北美）
        opening_weekend_US_and_Canada_date = opening_weekend_US_and_Canada_li.split(sep, 1)[1] #首映周末票房纪录（北美）日期
        #print(opening_weekend_US_and_Canada)
        #print(opening_weekend_US_and_Canada_date)
    except:
        opening_weekend_US_and_Canada = None
        opening_weekend_US_and_Canada_date = None
        #print(opening_weekend_US_and_Canada)
        #print(opening_weekend_US_and_Canada_date)
    try:
        gross_worldwide = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).get_text().strip().replace('Gross worldwide', '') #全球总票房
        #print(gross_worldwide)
    except:
        gross_worldwide = None
        #print(gross_worldwide)


    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=~.accdb;') #更改目录
    crsr = conn.cursor()
    sql = ("INSERT INTO top250 "
                "(imdb_id, title, startyear, movie_ratings, runtimeStr, imdb_rating, total_rating_amount, genres, plot, user_review_amount, critic_review_amount, metascore, budget, gross_US_and_Canada, opening_weekend_US_and_Canada, opening_weekend_US_and_Canada_date, gross_worldwide) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")  
    try:
        crsr.execute(sql,
            (
            tt, title, year, movie_ratings, runtimeStr, 
            imdb_rating, total_rating_amount, genres, plot, user_review_amount, 
            critic_review_amount, metascore, budget, gross_US_and_Canada, opening_weekend_US_and_Canada, 
            opening_weekend_US_and_Canada_date, gross_worldwide
            )
        )
        conn.commit()
        crsr.close()
        conn.close()
    except Exception as err:
        print(err)
        exit()

    print(i + 1, tt, '查找完成')

print('运行结束')
