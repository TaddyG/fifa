#Dashboard: https://your-published-link.render.com (password: soccer123)

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

#data
data = {
    "Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 
             1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    "Winner": ["Uruguay", "Italy", "Italy", "Uruguay", "West Germany", "Brazil", 
               "Brazil", "England", "Brazil", "West Germany", "Argentina", "Italy", 
               "Argentina", "West Germany", "Brazil", "France", "Brazil", "Italy", 
               "Spain", "Germany", "France", "Argentina"],
    "RunnerUp": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", 
                 "Czechoslovakia", "West Germany", "Italy", "Netherlands", "Netherlands", 
                 "West Germany", "West Germany", "Argentina", "Italy", "Brazil", "Germany", 
                 "France", "Netherlands", "Argentina", "Croatia", "France"]
}

df_wc = pd.DataFrame(data)

df_wc['Winner'] = df_wc['Winner'].replace({"West Germany": "Germany"})
df_wc['RunnerUp'] = df_wc['RunnerUp'].replace({"West Germany": "Germany"})

#count wins
winners_count = df_wc['Winner'].value_counts().reset_index()
winners_count.columns = ['Country', 'Wins']

#ISO codes for mapping purpsoes
country_iso = {
    "Uruguay": "URY",
    "Italy": "ITA",
    "Germany": "DEU",
    "Brazil": "BRA",
    "England": "GBR",
    "Argentina": "ARG",
    "France": "FRA",
    "Czechoslovakia": "CZE",  
    "Hungary": "HUN",
    "Sweden": "SWE",
    "Netherlands": "NLD",
    "Spain": "ESP",
    "Croatia": "HRV"
}

winners_count['ISO'] = winners_count['Country'].map(country_iso)

#create map
fig_choropleth = px.choropleth(
    winners_count,
    locations="ISO",
    color="Wins",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="FIFA World Cup Winners by Country"
)

#Creating layout

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA Soccer World Cup Dashboard", style={'textAlign': 'center'}),
    html.Hr(),
    
    #map section
    html.Div([
        dcc.Graph(id='choropleth-map', figure=fig_choropleth)
    ]),
    
    #show winning countries
    html.Div([
        html.H2("Countries that have won the World Cup:"),
        dash_table.DataTable(
            id='winner-table',
            columns=[{"name": col, "id": col} for col in winners_count.columns if col != 'ISO'],
            data=winners_count.to_dict('records'),
            style_table={'width': '50%', 'margin': 'auto'},
            style_cell={'textAlign': 'center'}
        )
    ], style={'padding': '20px'}),
    
    #selecting country
    html.Div([
        html.H2("Select a Country to View Number of Wins"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in winners_count['Country']],
            value='Brazil'
        ),
        html.Div(id='country-wins-output', style={'padding': '10px', 'fontSize': '20px', 'textAlign': 'center'})
    ], style={'padding': '20px'}),
    
    #selecting year
    html.Div([
        html.H2("Select a Year to View Finalists"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in df_wc['Year']],
            value=2018
        ),
        html.Div(id='year-output', style={'padding': '10px', 'fontSize': '20px', 'textAlign': 'center'})
    ], style={'padding': '20px'})
])

#callbakcs

#showing number of wins
@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def display_country_wins(selected_country):
    wins = winners_count.loc[winners_count['Country'] == selected_country, 'Wins'].values[0]
    return f"{selected_country} has won the World Cup {wins} times."

#winner and runner up
@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def display_year_finalists(selected_year):
    row = df_wc[df_wc['Year'] == selected_year]
    if not row.empty:
        winner = row['Winner'].values[0]
        runner_up = row['RunnerUp'].values[0]
        return f"In {selected_year}, the winner was {winner} and the runner-up was {runner_up}."
    else:
        return "Year not found."


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, dev_tools_prune_errors=False)

