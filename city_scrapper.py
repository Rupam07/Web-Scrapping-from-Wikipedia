import wikipedia, re
from bs4 import BeautifulSoup
import pandas as pd
import csv


def top_cities_in_US(parsed_table_data=None):
    "Get the details of top cities in US"
    wiki_page_title = "List of United States cities by population"
    n_columns = 0
    n_rows = 0
    column_names = []


    #Search wiki page
    search_results = wikipedia.page(wiki_page_title)
    # download the HTML source
    soup = BeautifulSoup(search_results.html(),features="lxml")

    #open csv file to write
    with open('city.csv', mode='w', encoding="utf-8") as city_file:
        writer = csv.writer(city_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        city_table = soup.find('table', {'class': 'wikitable sortable'})
        #print(city_table)

        rows = city_table.findAll('tr')
        td_tags = rows[0].find_all('th')

        if len(td_tags) > 0:
            n_rows += 1
            # Set the number of columns for our table
            n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = rows[0].find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text()[:-1])

        #hack ti include 2 cols dure to split cell
        column_names.append(" ")
        column_names.append(" ")
        #write column headers to the file
        writer.writerow(column_names)

        print(n_columns, n_rows)
        row_marker = 0

        #parse each row
        for i in range(1,len(rows)):
            row_data = []
            column_marker = 0
            columns = rows[i].find_all('td')
            city_title = []
            #parse each column
            for column in columns:

                row_data.append(column.get_text()[:-1])

                #to get page title
                if column_marker == 1:
                    city_title = re.findall("[\sA-Za-z]*",column.get_text()[:-1])
                column_marker += 1

            #get extra information about city page
            #city_result = wikipedia.page(city_title[0])
            #print(city_result.url)

            #write each row to the file
            writer.writerow(row_data)
            if len(columns) > 0:
                row_marker += 1



print('Top cities as per population data in the USA looks like this:\n\n')
top_cities_in_US()
