# Imports.--------------------------------------------------------------------------------------------------------------
import requests  # Import requests to access the web.
from bs4 import BeautifulSoup  # BeautifulSoup converts html code to a tree of python objects.
import pandas as pd  # Import pandas to create dataframes later.
import numpy as np  # Import numpy to arrange the page variable.
from time import sleep  # Import sleep to control the loop’s rate by pausing the execution of the loop.
from random import randint  # Import randint to vary the amount of waiting time between requests.

# Data storage.---------------------------------------------------------------------------------------------------------
titles = []  # The titles of the movies will be saved here.
years = []  # The year dates of the movies will be saved here.
time = []  # The time length of the movies will be saved here.
imdb_ratings = []  # The ratings of the movies will be saved here.
metascores = []  # The metascores of the movies will be saved here.
votes = []  # The votes of the movies will be saved here.
us_gross = []  # The USD gross of the movies will be saved here.

# Ensure we get English-translated titles from all the movies we scrape.------------------------------------------------
headers = {"Accept-Language": "en-US, en;q=0.5"}

# Variable of pages for loop iteration (stops at 951).------------------------------------------------------------------
pages = np.arange(1, 1001, 50)  # [1 51 101 151 ... 1001]

# Looping through each page.--------------------------------------------------------------------------------------------
for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page) + "&ref_=adv_nxt",
                        headers=headers)  # Build URL and fetch English-translated content only.
    soup = BeautifulSoup(page.text, 'html.parser')  # Convert the html code to a tree of objects of type BeautifulSoup.
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')  # Find all "div" tags with such class.
    sleep(randint(2, 10))  # Delays the loop execution by 2-10 seconds randomly.
    for container in movie_div:  # Loop for extracting all the data.
        name = container.h3.a.text
        titles.append(name)
        year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
        years.append(year)
        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else "-"
        metascores.append(m_score)
        nv = container.find_all('span', attrs={'name': 'nv'})
        vote = nv[0].text
        votes.append(vote)
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)

# Dataframe.------------------------------------------------------------------------------------------------------------
movies = pd.DataFrame({'movie': titles, 'year': years, 'imdb': imdb_ratings, 'metascore': metascores,
                       'votes': votes, 'us_grossMillions': us_gross, 'timeMin': time})

movies['votes'] = movies['votes'].str.replace(',', '').astype(int)

for z in range(0, len(movies['year'])):
    i = 0
    while not movies.loc[z, 'year'][i].isnumeric():
        i = i+1
    movies.loc[z, 'year'] = int(movies.loc[z, 'year'][i:i+4])

for z in range(0, len(movies['timeMin'])):
    i = 0
    temp = ""
    while movies.loc[z, 'timeMin'][i].isnumeric():
        temp = temp+movies.loc[z, 'timeMin'][i]
        i = i+1
    movies.loc[z, 'timeMin'] = int(temp.lstrip())

for k in range(0, len(movies['metascore'])):
    if movies.loc[k, 'metascore'] != "-":
        movies.loc[k, 'metascore'] = int(movies.loc[k, 'metascore'])
    else:
        movies.loc[k, 'metascore'] = np.nan

for m in range(0, len(movies['us_grossMillions'])):
    if movies.loc[m, 'us_grossMillions'] != "-":
        temp = movies.loc[m, 'us_grossMillions'].lstrip('$').rstrip('M')
        temp = temp
        movies.loc[m, 'us_grossMillions'] = float(temp)
    else:
        movies.loc[m, 'us_grossMillions'] = np.nan

movies.to_csv('movies.csv', index=False)

print(movies.isnull().sum())
