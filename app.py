import re
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

pd.set_option('display.max_columns', None)  

# Load data
df = pd.read_excel("Data//CANDEV_PSC data.xlsx")

# Find unique labels for each category 
df = df.sort_values(by=['ORGANISATION', 'APPLICATION DATE / DATE DE CANDIDATURE'])
orgs = df['ORGANISATION'].sort_values().unique()
levels = df['GROUP AND LEVEL  / GROUPE ET NIVEAU'].sort_values().unique()
provinces = df['PROVINCE_EN'].sort_values().unique()
languages = df['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)'].sort_values().unique()
groups = ['MEMBERS OF VISIBLE MINORITIES / MINORITÉS VISIBLES','INDIGENOUS PEOPLES / AUTOCHTONES','PERSONS WITH DISABILITIES / PERSONNES EN SITUATION DE HANDICAP']

# Format data
df['ORGANISATION']=df['ORGANISATION'].astype('string')
df['GROUP AND LEVEL  / GROUPE ET NIVEAU']=df['GROUP AND LEVEL  / GROUPE ET NIVEAU'].astype('string')
df['PROVINCE_FR']=df['PROVINCE_FR'].astype('string')
df['PROVINCE_EN']=df['PROVINCE_EN'].astype('string')
df['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)']=df['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)'].astype('string')
df['MEMBERS OF VISIBLE MINORITIES / MINORITÉS VISIBLES'] = df['MEMBERS OF VISIBLE MINORITIES / MINORITÉS VISIBLES'].astype('bool')
df['INDIGENOUS PEOPLES / AUTOCHTONES'] = df['INDIGENOUS PEOPLES / AUTOCHTONES'].astype('bool')
df['PERSONS WITH DISABILITIES / PERSONNES EN SITUATION DE HANDICAP'] = df['PERSONS WITH DISABILITIES / PERSONNES EN SITUATION DE HANDICAP'].astype('bool')

# Initialize dash app
app = Dash(__name__)

# HTML layout
app.layout = html.Div(children=[

    # Title 
    html.H1(children='PSC Dashboard'),

    # Sub heading
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    # Province list
    html.Div(children=[
        html.Br(),
        html.Label('Provinces'),
        dcc.Checklist(
            options=provinces,
            value=provinces[0:2],
            id='select_prov'
        )
    ], style={'padding': 5, 'flex': 1}),

    # Language list
    html.Div(children=[
        html.Br(),
        html.Label('Languages'),
        dcc.Checklist(
            options=languages,
            value=languages,
            id='select_lang'
        )
    ], style={'padding': 5, 'flex': 1}),

    # Levels list
    html.Div(children=[
        html.Br(),
        html.Label('Levels'),
        dcc.Checklist(
            options=levels,
            value=levels,
            id='select_lvl'
        )
    ], style={'padding': 5, 'flex': 1}),

    # Figure
    dcc.Graph(
        id='fig',
    ),
])

# Callbacks for dashboard interaction
@app.callback(
    Output('fig','figure'),
    Input('select_prov','value'),
    Input('select_lang','value'),
    Input('select_lvl','value')
)

# Ploting and figure update
def update_graph(select_prov,select_lang,select_lvl):
    # Format selected categories and seperate by OR (|)
    temp_str = '|'.join(select_prov)
    provs = re.sub("[\(\[].*?[\)\]]", "", temp_str)
    langs = '|'.join(select_lang)
    lvls = '|'.join(select_lvl)

    # Query df
    dff = df[df['PROVINCE_EN'].str.contains(provs)]
    dff = dff[dff['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)'].str.contains(langs)]
    dff = dff[dff['GROUP AND LEVEL  / GROUPE ET NIVEAU'].str.contains(lvls)]

    # Generate org hist, extract traces
    fig1 = px.histogram(dff, x='ORGANISATION')
    fig1.update_layout(bargap=0.2)
    figure1_traces = []
    for trace in range(len(fig1["data"])):
        figure1_traces.append(fig1["data"][trace])

    # Generate salargy hist, extract traces
    fig2 = px.histogram(dff, x='SALARY / SALAIRE', nbins=20, color_discrete_sequence=['indianred'])
    fig2.update_layout(bargap=0.2)
    figure2_traces = []
    for trace in range(len(fig2["data"])):
        figure2_traces.append(fig2["data"][trace])

    # Plot figures
    fig = sp.make_subplots(
        rows=1, cols=2)

    for traces in figure1_traces:
        fig.append_trace(traces, row=1, col=1)

    for traces in figure2_traces:
        fig.append_trace(traces, row=1, col=2)

    # Update figure layout
    fig.update_layout(bargap=0.1)
    fig.update_layout(height=600, width=1500, title_text="Application Histograms by Organisation and Salary")

    # Update xaxis properties
    fig.update_xaxes(title_text="Salargy Ranges", row=1, col=2)
    fig.update_xaxes(title_text="Organisations", row=1, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Number of Applicants", row=1, col=1)
    fig.update_yaxes(title_text="Number of Applicants", row=1, col=2)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)