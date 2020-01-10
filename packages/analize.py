######################################### IMPORTING LIBRARIES #################################################
import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pandas_datareader import wb


### Getting clean data:
def enriching_data(proc_data):

    #### > Importing Json from Forbes.com to get 'country'
    forbes_url = 'https://www.forbes.com/ajax/list/data?year=2018&uri=billionaires&type=person'
    df = pd.read_json(forbes_url, orient='records')
    # id_country.head(20)
    name_country = df[['name', 'country', ]]
    name_country.name = name_country.name.str.upper()
    # Merging this table with proc_data
    enriched_data = pd.merge(proc_data, name_country, left_on='FullName', right_on='name')
    enriched_data.drop('name', axis=1)

    ### Aggregation of enriched data
    top = input('Please enter the number of top millionaries: ')  # until 1000 works well

    # Considering all position values over 'top' value, grouping Worth by Country, and sorting values
    meanW_country = enriched_data[enriched_data['position'] <= top].groupby('country')['worth_BUSD'].mean().sort_values(
        ascending=False)

    # Converting 'Industry' as index to column, to represent in bar plot
    meanW_country = meanW_country.reset_index()
    meanW_country.rename(columns={'worth_BUSD': 'mean_worth_BUSD'}, inplace=True)

    #Listing countries
    country_list = list(meanW_country.country.unique())

    # WEBSCRAPING: Wikipedia > country code
    url = 'https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all('table', {'class': 'wikitable sortable'})[0]

    # tr represent the table rows
    rows = table.find_all('tr')
    rows_parsed = [row.text for row in rows]

    def smart_parser(row_text):
        row_text = row_text.replace('\n\n', '\n').strip('\n')

        # Erasing some exceptions
        row_text = re.sub('.mw-parser-output .monospaced{font-family:monospace,monospace}', '', row_text)
        row_text = re.sub('\[ah\]', '', row_text)
        row_text = re.sub('Hong Kong SAR, China', 'Hong Kong', row_text)

        return list(map(lambda x: x.strip(), row_text.split('\n')))

    well_parsed = list(map(lambda x: smart_parser(x), rows_parsed))

    for x in well_parsed:
        if len(x) != 8:
            well_parsed.remove(x)  # only get list wich contains information about countries

    colnames = ['Countries', 'b1', 'b2', '2L', '3L', 'b3', 'b4', 'b5']
    data = well_parsed[1:]
    country_codes = pd.DataFrame(data, columns=colnames)
    country_codes.drop(columns=['b1', 'b2', 'b3', 'b4', 'b5'], inplace=True)

    #Merging the codes with the initial df
    meanW_country = pd.merge(meanW_country, country_codes, left_on='country', right_on='Countries')
    meanW_country.drop(columns=['Countries'], inplace=True)

    ## API: World Bank > Getting info about GDP per country
    matches = wb.search('gdp.*capita.*const')
    countries_GDP = list(meanW_country['2L'].unique())

    WB_data = wb.download(indicator='NY.GDP.PCAP.CD', country=countries_GDP, start=2018, end=2018)
    WB_data = WB_data.reset_index()
    WB_data.drop('year', axis=1)
    WB_data.rename(columns={'NY.GDP.PCAP.CD': 'GDP_USD', 'country': 'country_gdp'}, inplace=True)

    #Finally merging all the tables
    meanW_GDPP = pd.merge(meanW_country, WB_data, left_on='country', right_on='country_gdp')
    meanW_GDPP.drop(columns=['year', 'country_gdp', '3L'], inplace=True)
    meanW_GDPP['ratio_MUSD'] = meanW_GDPP['mean_worth_BUSD'] * 1000000 / meanW_GDPP['GDP_USD']
    meanW_GDPP.sort_values(by='ratio_MUSD', ascending=False, inplace=True)
    meanW_GDPP.reset_index().drop(columns=['index'], inplace=True)

    table = meanW_GDPP

    return table,top