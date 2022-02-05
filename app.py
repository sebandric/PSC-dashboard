from re import S
import numpy as np
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


pd.set_option('display.max_columns', None)  

salary_bins = []

# Load data, change identity groups to boolean
df = pd.read_excel("Data//CANDEV_PSC data.xlsx")

df['ORGANISATION']=df['ORGANISATION'].astype('string')
df['GROUP AND LEVEL  / GROUPE ET NIVEAU']=df['GROUP AND LEVEL  / GROUPE ET NIVEAU'].astype('string')
df['PROVINCE_FR']=df['PROVINCE_FR'].astype('string')
df['PROVINCE_EN']=df['PROVINCE_EN'].astype('string')
df['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)']=df['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)'].astype('string')
df['MEMBERS OF VISIBLE MINORITIES / MINORITÉS VISIBLES'] = df['MEMBERS OF VISIBLE MINORITIES / MINORITÉS VISIBLES'].astype('bool')
df['INDIGENOUS PEOPLES / AUTOCHTONES'] = df['INDIGENOUS PEOPLES / AUTOCHTONES'].astype('bool')
df['PERSONS WITH DISABILITIES / PERSONNES EN SITUATION DE HANDICAP'] = df['PERSONS WITH DISABILITIES / PERSONNES EN SITUATION DE HANDICAP'].astype('bool')
df = df.sort_values(by=['ORGANISATION', 'APPLICATION DATE / DATE DE CANDIDATURE'])

# Find unique labels for each category 
orgs = df['ORGANISATION'].unique()
levels = df['GROUP AND LEVEL  / GROUPE ET NIVEAU'].unique()
provinces = df['PROVINCE_EN'].unique()
languages = df['FIRST OFFICIAL LANGUAGE / PREMIÈRE LANGUE OFFICIELLE (EN)'].unique()

app = Dash(__name__)

fig = px.histogram(df, x='ORGANISATION')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)