import pandas as pd
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server

# ------------------------------------------------------------------------------

unemployment_df = pd.read_csv("https://raw.githubusercontent.com/ChefPaul/CUNY_DATA_608/master/Final%20Project/Paul%20Perez%20Final%20Project/data/weekly_unemployment.csv")
unemployment_df = unemployment_df[unemployment_df["Date"] >= "2019-07-01"]

stock_df = pd.read_csv('https://raw.githubusercontent.com/ChefPaul/CUNY_DATA_608/master/Final%20Project/Paul%20Perez%20Final%20Project/data/stock_data.csv')
stock_df = stock_df[stock_df["Date"] >= "2019-07-01"]

# ------------------------------------------------------------------------------


# App Layout
app.layout = html.Div([
    
    html.Br(),
    html.H1("COVID-19's Impact on the U.S. Economy", style={"text-align":"center"}),
    html.Br(),
    html.Br(),
    
    html.H3("An Abridged Recap of Events", style={"text-align":"center"}),
    html.H6("February 2nd, 2020: U.S. enacted travel restrictictions to and from China.", style={"text-align":"center"}),
    html.H6("February 25th, 2020: CDC Warned American public to prepare for local outbreak.", style={"text-align":"center"}),
    html.H6("March 2nd, 2020: Travel restrictions from Iran went into effect.", style={"text-align":"center"}),
    html.H6("March 11th, 2020: World Health Organization declared a pandemic.", style={"text-align":"center"}),
    html.H6("March 12th, 2020: Diagnosed cases of COVID-19 in the U.S. exceed a thousand.", style={"text-align":"center"}),
    html.Br(),
    
    
    html.H2("Unemployment Claims Surge in March and April Amid Layoffs and Lockdowns", style={"text-align":"center"}),
    
    html.Div([

            dcc.Graph(id="unemployment-chart",
                     figure={
                         "data":[
                                 {"x":unemployment_df["Date"],
                                  "y":unemployment_df["Claims"],
                                  "type":"bar",
                                  "name":"Job Claims",
                                  "template":"simple_white"}
                         ],
                         "template":"simple_white"
                     },
                     ),
            html.H6("April see's 23,078,00 unemployment claims", style={"text-align":"center"}),
        html.H6("Data provided by the Federal Reserve Bank of St. Louis", style={"text-align":"center"}),
        dcc.Link("Federal Reserve Bank of St. Louis Economic Research", href="https://fred.stlouisfed.org/series/ICSA"),
            
                       ],style={"width":"100%",
                 "text-align":"center",
                 "verticalAlign":"center",
                 "justify-content":"center"}),

            
    
    
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2("U.S. Stock Market Crashes Providing Opportunity for New Retail Investors", style={"text-align":"center"}),
    html.Br(),

    html.Div([
        
        html.Div([

            dcc.Graph(id="candle-chart"),

            ],style={"width":"100%", 
                     "verticalAlign":"center"})
        
    ],style={"text-align":"center",
             #"display":"flex",
             "justify-content":"center"}),
    
    html.Div([
            
            html.H3("Select a Market", style={"text-align":"center"}),
            
            html.Br(),
            
            html.Div([
                dcc.Dropdown(
                    id="dropdown",
                    options=[
                            {"label": "Nasdaq", "value": "IXIC"},
                            {"label": "S&P 500", "value": "GSPC"},
                            {"label": "Dow Jones", "value": "DJI"}
                    
                    ],
                    value="IXIC",
                    clearable=False,
                    placeholder="Please select a market...",
                    style={"text-align":"center",
                           "verticalAlign":"center",
                           "justify-content":"center",
                           "align-items":"center"}
                           #""}
                            #"display": "inline-block"}
                    ),

                    ],style={"width":"25%",
                             "text-align":"center",
                             "verticalAlign":"center",
                             "display":"inline-block"}),

            html.Br(),
            html.Br(),
            html.H6("Use the range selector above to change the date range"),
            html.H6("Click on an item from the legend to toggle it into the view"),
            html.H6("By plotting both EMA and SMA on a price chart, you can spot a possible turn in a stock price. (Link Below)", style={"text-align":"center"}),
            dcc.Link("What Is 'EMA' in Stock Trading - ZACKS", href="https://finance.zacks.com/ema-stock-trading-9900.html#:~:text=By%20plotting%20both%20EMA%20and%20SMA%20on%20a,is%20falling%29%20and%20price%20resistance%20%28when%20it%27s%20rising%29."),
            html.H6("Data provided Pandas DataRader", style={"text-align":"center"}),
            dcc.Link("Pandas DataReader", href="https://pandas-datareader.readthedocs.io/en/latest/"),

            html.Br(),
            html.Br(),
            html.Br(),
            html.H6("Dash App Created by: Paul Perez - CUNY SPS M.S. Data Science, 2021", style={"text-align":"center"}),
            dcc.Link("GitHub Repository", href="https://github.com/ChefPaul/CUNY_DATA_608/tree/master/Final%20Project/Paul%20Perez%20Final%20Project"),
        
        
        
        ],style={"width":"100%",
                 "text-align":"center",
                 "verticalAlign":"center",
                 "justify-content":"center"}),
            
            html.Br(),
    
            html.Br(),

       
])

# ------------------------------------------------------------------------------

# Connect to Plotly graphs with Dash Components
@app.callback(
    Output("candle-chart", "figure"), 
    [Input("dropdown", "value")])

def update_candle_chart(dropdown):
    dff = stock_df
    dff = dff[dff["Ticker"] == str(dropdown)]
    start_date = dff["Date"].min()
    end_date = dff["Date"].max()
    
    sma = dff.Close.rolling(window = 50).mean()
    ema = dff.Close.ewm(span=12, adjust=False).mean()
    
    data=[go.Candlestick(x=dff['Date'],
                open=dff['Open'],
                high=dff['High'],
                low=dff['Low'],
                close=dff['Close'])]
    
    layout = dict(
        title=f"<b>{dropdown}<b> <br> {start_date} to {end_date}",
        title_x=0.5,
        xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Date")),
        yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Price $ - U.S. Dollars")),
        shapes = [dict(x0='2020-02-25', x1='2020-02-25', y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
        annotations=[dict(x='2020-02-25', y=0.95, xref='x', yref='paper',
        showarrow=False, xanchor='left', text='CDC Warns America to Prepare for Outbreak')])
                         
        
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(name=f"{dropdown}", selector=dict(type="candlestick"))
    
    fig.add_scatter(x=dff['Date'],
                        y=sma,
                        mode='lines',
                        name='SMA - 50'),

        
    fig.add_scatter(x=dff['Date'],
                        y=ema,
                        mode='lines',
                        name='EMA - 12')
    
    fig.update_layout(template="simple_white")
    fig.update_layout(hovermode="x unified")
    
    return fig
    
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server()