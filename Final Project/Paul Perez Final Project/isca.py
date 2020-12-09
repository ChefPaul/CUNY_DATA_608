import json
import pandas as pd
import pandas_datareader.data as web
import requests


def get_icsa_data_fred(key):
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id=ICSA&api_key={key}&file_type=json'
    response = requests.get(url)
    data = response.json()
    
    weeks = []
    claims = []
    
    for i in data['observations']:
        weeks.append(i['date'])
        claims.append(i['value'])

    dict = {"Date": weeks,
            "Claims": claims}    
        
    df = pd.DataFrame(dict)    
        
    return df

def main():

    key = 'YOUR KEY HERE'
    icsa = get_icsa_data_fred(key)
    icsa.to_csv('./data/weekly_unemployment.csv', index=False) 

if __name__ == '__main__':
    main() 