import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash(__name__)

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
trees.dropna(inplace = True)

tr1 = trees[['boroname', 'spc_common', 'health']]
tr2 = trees[['spc_common', 'health', 'steward']]
hs = tr2.groupby(['spc_common', 'health'])

species = tr1['spc_common'].str.capitalize().unique()
borough = tr1['boroname'].unique()
health = tr2['health'].unique()
colors = ["#006D2C", "#31A354", "#74C476", "#90D691"]
tg = tr1.groupby(['spc_common', 'boroname'])

app.layout = html.Div(children=[ 
    html.H1(children='Data 608: Module 4 | Interactive Visualizations in Python'),
    html.H4(children='Paul Perez'),
    html.H5(children='''In this module we’ll be looking at data from the New York City tree census:  
 
                        https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
                     '''),
    html.H5(children='''
                        This data is collected by volunteers across the city, and is meant to catalog information about every single tree in the city.
                        The idea is to build a dash app for a arborist studying the health of various tree species (as defined by the variable ‘spc_common’) 
                        across each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each species and in each borough: 
                        '''),

    html.Div(children='''
        Question 1:  What proportion of trees are in good, fair, or poor health according to the ‘health’ variable?
    '''),

    dcc.Dropdown(
         id="tree_type",
         options=[{'label': i, 'value': i} for i in species],
         placeholder = 'Select A Tree'
         ),
    
    dcc.Dropdown(
         id="borough",
         options=[{'label': i, 'value': i} for i in borough],
         placeholder = 'Select A Borough'
         ),
       
     dcc.Graph(
        id = 'health_graph'    
    ),
     
    html.Div(children='''
        Question 2:   Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees? 
     '''),
     
     dcc.Dropdown(
         id="tree_type2",
         options=[{'label': i, 'value': i} for i in species],
         placeholder = 'Select A Tree'
         ),
    
    dcc.Dropdown(
         id="health",
         options=[{'label': i, 'value': i} for i in health],
         placeholder = 'Select A Health Element'
         ),
    
        dcc.Graph(
        id = 'steward_graph'    
    )
    
])

@app.callback(
    dash.dependencies.Output('health_graph', 'figure'),
    [dash.dependencies.Input('tree_type', 'value'),
    dash.dependencies.Input('borough', 'value')])

def update_graph(selected, selected2):
    trace = go.Pie(labels = tg.get_group((selected, selected2))['health'].unique() , 
                   values = tg.get_group((selected, selected2))['health'].value_counts())
    data = [trace]
    fig = go.Figure(data = data)
    return fig


@app.callback(
    dash.dependencies.Output('steward_graph', 'figure'),
    [dash.dependencies.Input('tree_type2', 'value'),
    dash.dependencies.Input('health', 'value')])

def update_graph2(selected, selected2):
   trace2 = go.Bar(x = hs.get_group((selected, selected2))['steward'].unique(),
                   y = hs.get_group((selected, selected2))['steward'].value_counts(), 
                   marker={'color': colors})
   data = [trace2]
   fig2 = go.Figure(data = data)
   return fig2


if __name__ == '__main__':
    app.run_server()