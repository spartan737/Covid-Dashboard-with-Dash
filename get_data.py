import requests
import pandas as pd
import dash_html_components as html


def latest_covid_data(csv_file):
    df = pd.read_csv(csv_file)

    # Identify rows that have new cases less than 0, which is impossible
    df[df['new_cases'] < 0] = 0

    # Get just the relevant columns
    df = df[["iso_code", "continent", "location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths",
             "total_cases_per_million", "new_cases_per_million", "total_deaths_per_million", "new_deaths_per_million",
             "population", "total_vaccinations"]]

    # Continent that are N.A. means total world statistics
    df = df[df['continent'].notna()]

    # Remove rows that are wrong value / empty
    df = df[df['date'].notna()]
    df = df[df['date'] != 0]
    df = df.round(2)

    # Replace all N.A. with 0 for easy manipulation of data
    df.fillna(0, inplace=True)
    # df.to_csv('covid-data.csv')

    # Convert column from string to date object
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    # group_continent = pd.read_csv('covid-data.csv')

    country_name_list = []
    for country_name in df['location'].unique():
        country_name_list.append({'label': country_name, 'value': country_name})

    # transform every unique date to a number
    numdate = [x for x in range(0, len(df['date'].unique()) + 30, 30)]

    return df, country_name_list, numdate


def generate_thumbnail(news_title, news_url, news_image_url):
    return html.Div([
        html.Img(src=news_image_url,
                 style={"width": "100%"}),
        html.A(news_title, href=news_url, target='_blank'),
    ], className="newspaper_thumbnail")


def latest_news(df):
    all_news = []
    url = ('http://newsapi.org/v2/everything?'
           'language=en&'
           'q=covid-19&'
           'from={}'
           'sources=bbc-news&'
           'sortBy=popularity&'
           'apiKey=bf25476268b640d0a6972e685f1c7215'.format(df['date'].max()))

    response = requests.get(url)

    for news in response.json()['articles']:
        if 'vaccine' in news['title'].lower() or 'vaccination' in news['title'].lower() \
                or 'coronavirus' in news['title'].lower() or 'covid' in news['title'].lower() or 'lockdown' in news['title'].lower():
            title = news['title']
            # print(title, 'TITLE', len(title))
            # if len(news['title']) <= 39:
            #     title = news['title'] + ' &#10;'
            # print(title)
            all_news.append(generate_thumbnail(title, news['url'], news['urlToImage']))
    return all_news