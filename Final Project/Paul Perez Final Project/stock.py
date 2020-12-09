import pandas as pd
import pandas_datareader.data as web

def get_stock_data(start, end, ticker):
        
    df = web.DataReader(name=ticker, data_source='yahoo', start=start, end=end)
    df.reset_index(level=0, inplace=True)
    df['Ticker'] = str(ticker).replace("^","")
    df = df[df.columns[[7,0,1,2,3,4,5,6]]]

    return df

def main():
    start = '2005-01-01'
    end = '2020-12-07'
    ticker = ['^IXIC','^GSPC', '^DJI']

    df_ixic = get_stock_data(start,end,ticker[0])
    df_gspc = get_stock_data(start,end,ticker[1])
    df_djia = get_stock_data(start,end,ticker[2])

    df = pd.concat([df_ixic,df_gspc,df_djia], ignore_index=True)
    df.to_csv('./data/stock_data.csv', index=False)

if __name__ == '__main__':
    main()