# Deployed Link: https://your-render-link-here.com (replace with your actual deployed app link)


import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback

# Dataset 
data = [
    [1930, "Uruguay", "Argentina"],
    [1934, "Italy", "Czechoslovakia"],
    [1938, "Italy", "Hungary"],
    [1950, "Uruguay", "Brazil"],
    [1954, "Germany", "Hungary"],
    [1958, "Brazil", "Sweden"],
    [1962, "Brazil", "Czechoslovakia"],
    [1966, "England", "Germany"],
    [1970, "Brazil", "Italy"],
    [1974, "Germany", "Netherlands"],
    [1978, "Argentina", "Netherlands"],
    [1982, "Italy", "Germany"],
    [1986, "Argentina", "Germany"],
    [1990, "Germany", "Argentina"],
    [1994, "Brazil", "Italy"],
    [1998, "France", "Brazil"],
    [2002, "Brazil", "Germany"],
    [2006, "Italy", "France"],
    [2010, "Spain", "Netherlands"],
    [2014, "Germany", "Argentina"],
    [2018, "France", "Croatia"],
    [2022, "Argentina", "France"]
]

df = pd.DataFrame(data, columns=["Year", "Winner", "RunnerUp"])



winner_counts = df['Winner'].value_counts().reset_index()
winner_counts.columns = ['Country', 'Wins']


# The Dash App 
app = Dash(__name__)

fig = px.choropleth(
    winner_counts,
    locations='Country',
    locationmode='country names',
    color='Wins',
    color_continuous_scale='Viridis',
    title='Countries with FIFA World Cup Wins'
    )

fig.update_traces(
    hovertemplate = "Country: %{location}<br>Wins: %{z}<extra></extra>"
    )


app.layout = html.Div([
    html.H1("FIFA World Cup Winners", style={'textAlign': 'center'}),

    html.H2("Map of World Cup Winners"),

    dcc.Graph(id='choropleth-map', figure=fig),

    html.H2("Check Wins by Country"),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(winner_counts['Country'].unique())],
        value='Brazil'
    ),

    html.Div(id='country-win-output'),


    html.H2("Check Wins and Runner-Up by Year"),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(y), 'value': y} for y in df['Year']],
        value=2022
    ),

    html.Div(id='year-result-output')

])


@callback(
    Output('country-win-output', 'children'),
    Input('country-dropdown', 'value')
)


def update_country_wins(selected_country):
    
    wins = winner_counts[winner_counts['Country'] == selected_country]['Wins'].values
    
    count = int(wins[0]) if len(wins) > 0 else 0
    
    return html.Div([
        html.Strong(selected_country),
        " FIFA World Cup wins", 
        ": ", 
        html.Strong(str(count))
    ])


@callback(
    Output('year-result-output', 'children'),
    Input('year-dropdown', 'value')
)


def update_year_result(selected_year):

    row = df[df['Year'] == selected_year]

    if not row.empty:
        winner = row.iloc[0]['Winner']
        runnerup = row.iloc[0]['RunnerUp']

        return html.Div([

            html.P([

                "In ",
                html.Strong(str(selected_year)),
                ", ",
                html.Strong(winner),
                " won the FIFA World Cup."

            ]),


            html.P([

                html.Strong(runnerup),
                " was the runner-up."

            ])
]) 
        
    return "No data available for this year."

# Running the Server 
if __name__ == '__main__':
    app.run(debug=True)


