import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

data = pd.read_csv('modified.csv')

total = ['All Years']
years = [i for i in range(2005,2020,1)]
all = total + years

# Sidebar style on the left
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "3rem 1rem",
    "background-color": "#c2c2c2",
}

# Content style on the right
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(),
        
        # Options
        html.Div(children=[
            # Choose Country
            html.Div(children=[
                html.H4('Choose Country:'),
                dcc.Dropdown(id='country',
                            options=[
                                {'label':'All Countries', 'value':'AC'},
                                {'label':'Kenya', 'value':'Kenya'},
                                {'label':'Rwanda', 'value':'Rwanda'},
                                {'label':'Ghana', 'value':'Ghana'}
                            ],
                            value ='AC')
            ]),
            
            # Choose Region
            html.Div(children=[
                html.H4('Choose Region:'),
                dcc.Dropdown(id='region',
                            options=[
                                {'label':'National', 'value':'National'},
                                {'label':'Urban', 'value':'Urban'},
                                {'label':'Rural', 'value':'Rural'}
                            ],
                            value ='National')
            
            ]),
            
            # Choose Year
            html.Div(children=[
                html.H4('Choose Year:'),
                dcc.Dropdown(id='year',
                            options=[
                                {'label':i, 'value': i} for i in all],
                            value ='All Years')
            ])
        ]),
           
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(children=[
    # Dashboard title
    html.Div(html.H2('YOUTH EMPLOYMENT IN RURAL AND URBAN AREAS IN TERMS OF SEX AND ECONOMIC ACTIVITY', style={'textAlign':'center'})),
    html.Hr(), 
    # Graph
    html.Div(children=[
        html.Div(id='plot')
    ])

], style=CONTENT_STYLE)

# Initializing the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Creating the app layout
app.layout = html.Div(children=[sidebar, content])


# App Callback
@app.callback(Output(component_id='plot', component_property='children'),
              
             [Input(component_id='country', component_property='value'),
             Input(component_id='region', component_property='value'),
             Input(component_id='year', component_property='value')],
              
             State(component_id='plot', component_property='children'))


def get_graph(country, region, year, children):
    
    if country == 'AC' or year == 'All Years':
        
        if country == 'AC' and year == 'All Years':
            df = data[(data['region']==region)]
            avg_val = df.groupby(['activity','sex'])['obs_value'].sum().reset_index()
            fig = px.bar(avg_val, x='activity', y='obs_value', color='sex', barmode='group')
            return dcc.Graph(figure=fig)
        
        elif country == 'AC':
            df = data[(data['region']==region) & (data['year']==year)]
            avg_val = df.groupby(['activity','sex'])['obs_value'].sum().reset_index()
            fig = px.bar(avg_val, x='activity', y='obs_value', color='sex', barmode='group')
            return dcc.Graph(figure=fig)
        
        
        elif year == 'All Years':
            df = data[(data['country']== country) & (data['region']==region)]
            avg_val = df.groupby(['activity','sex'])['obs_value'].sum().reset_index()
            fig = px.bar(avg_val, x='activity', y='obs_value', color='sex', barmode='group')
            return dcc.Graph(figure=fig)
              
    else:
        df = data[(data['country']== country) & (data['region']==region) & (data['year']==year)]
        avg_val = df.groupby(['activity','sex'])['obs_value'].sum().reset_index()
        fig = px.bar(avg_val, x='activity', y='obs_value', color='sex', barmode='group')
        return dcc.Graph(figure=fig)


# Running the app
if __name__ == '__main__':
    app.run_server()
