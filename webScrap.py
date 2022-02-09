import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create an URL object
url = 'https://edge.pse.com.ph/companyPage/stockData.do?cmpy_id=57'
# Create object page
page = requests.get(url)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')

# Obtain information from tag <table>
table1 = soup.find('table')

# Obtain every title of columns with tag <th>
headers = ['Ticker']
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)

# Create a dataframe
mydata = pd.DataFrame(columns=headers)

for id in range(1, 500):
    url2 = f'https://edge.pse.com.ph/companyPage/stockData.do?cmpy_id={id}'
    print(url2)

    # Create object page
    page2 = requests.get(url2)

    # parser-lxml = Change html to Python friendly format
    # Obtain page's information
    soup2 = BeautifulSoup(page2.text, 'lxml')

    # Obtain information from tag <table>
    table2 = soup2.find('table')

    if table2 != None:
        data = {}
        # Create a for loop to fill mydata
        for j in table2.find_all('tr'):
            row_header = j.find_all('th')
            row_data = j.find_all('td')

            for i in range(len(row_header)):
                value = row_data[i].text.strip('\r\n').strip()

                data[row_header[i].text] = value

        stockName = soup2.find('select').find_all(selected=True)[0].text
        data["Ticker"] = stockName

        mydata = mydata.append(data, ignore_index=True)

mydata.to_csv('result.csv', index=False)
mydata.to_excel('result.xlsx', index=False)
