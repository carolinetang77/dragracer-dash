import plotly.express as px
import pandas as pd
from dash import dash, dcc, html, Input, Output, State

# import data 
dr_data = pd.read_csv('data/drag.csv', index_col=0)

# remove all episodes where queens didn't compete
dr_data = dr_data[dr_data['participant'].apply(lambda x: x == 1)]

dob = (
    dr_data[['season', 'rank', 'contestant', 'outcome']]
    .groupby(['season', 'rank', 'contestant'])
    .value_counts(['outcome'])
    .reset_index(name = 'count')
    .pivot(index = ['season', 'rank', 'contestant'], columns = 'outcome', values = 'count')
    .reset_index()
    .fillna(0)
)
dob['dob'] = 2 * dob['WIN'] + dob['HIGH'] - dob['LOW'] - 2 * dob['BTM']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Drag Race Visualizer'),
    html.Label('Seasons:'),
    dcc.Dropdown(
        id = 'season', 
        options = sorted(dr_data['season'].unique()),
        value = 'S01',
        multi=True,
        placeholder='Select one or more seasons to compare'
    ),
    html.Br(),
    html.Label('Queens:'),
    dcc.Dropdown(
        id = 'queen', 
        options = sorted(dr_data['contestant'].unique()),
        value = 'Jinkx Monsoon',
        multi=True,
        placeholder='Select one or more queens to compare'
    ),
    dcc.Graph(
        id = 'performance'
    )
])

@app.callback(
    Output('queen', 'options'),
    Output('queen', 'value'),
    Input('season', 'value'),
    State('queen', 'value')
)
def update_queens(season, queens):
    if season is not None and len(season) != 0:
        seasonal = dr_data.query("season in @season")
        options = sorted(seasonal['contestant'].unique())
        values = seasonal.sort_values('rank')['contestant'].unique()[:2]
    else:
        options = sorted(dr_data['contestant'].unique())
        if queens is None or len(queens) == 0:
            values = dr_data.query("winner == 1")['contestant'].unique()
        else:
            values = queens
    return options, values

@app.callback(
    Output('performance', 'figure'),
    Input('season', 'value'),
    Input('queen', 'value')
)
def plot_performance(season, queen):
    filtered = dob
    if season is not None and len(season) != 0:
        filtered = dob.query("season in @season")
    
    if queen is not None and len(queen) != 0:
        filtered = dob.query("contestant in @queen")
    
    fig = px.bar(
        filtered.sort_values(['rank', 'dob'], ascending = [False, True]),
        x = 'dob',
        y = 'contestant',
        color = 'dob',
        color_continuous_scale='Plotly3',
        title = 'Contestant Performance Scores',
        labels = {
            'dob': 'Dusted or Busted Score',
            'season': 'Season',
            'contestant': 'Queen',
            'rank': 'Rank',
            'WIN': 'Wins',
            'HIGH': 'High',
            'LOW': 'Low',
            'BTM': 'Bottom'
        },
        hover_name = 'contestant',
        hover_data = {'contestant': False, 'season': True, 'rank': True, 'WIN': True, 'HIGH': True, 'LOW': True, 'BTM': True})
    
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)