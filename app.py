import plotly.express as px
import pandas as pd
from dash import dash, dcc, html, Input, Output

# import data
dr_data = pd.read_csv('data/drag.csv', index_col=0)
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
        multi=True,
        placeholder='Select one or more queens to compare'
    ),
    dcc.Graph(
        id = 'performance'
    )
])

@app.callback(
    Output('queen', 'options'),
    Input('season', 'value')
)
def update_queens(season):
    if season is not None and len(season) != 0:
        options = sorted(dr_data[dr_data['season'].apply(lambda x: x in season)]['contestant'].unique())
    else:
        options = sorted(dr_data['contestant'].unique())
    return options

@app.callback(
    Output('performance', 'figure'),
    Input('season', 'value'),
    Input('queen', 'value')
)
def plot_performance(season, queen):
    # remove all episodes where queens didn't compete
    filtered = dr_data[dr_data['participant'].apply(lambda x: x == 1)]

    if season is not None and len(season) != 0:
        filtered = filtered[filtered['season'].apply(lambda x: x in season)]
    
    if queen is not None and len(queen) != 0:
        filtered = filtered[filtered['contestant'].apply(lambda x: x in queen)]
    
    fig = px.line(
        filtered.sort_values('episode'),
        x = 'episode',
        y = 'outcome',
        color = 'contestant',
        markers = True,
        title = 'Contestant Outcomes',
        labels = {
            'season': 'Season',
            'episode': 'Episode Number',
            'outcome': 'Episode Outcome',
            'contestant': 'Queen'
        },
        hover_name = 'contestant',
        hover_data = {'contestant': False, 'season': True, 'episode': True, 'outcome': True})
    
    fig.update_yaxes(
        type='category', 
        categoryorder='array', 
        categoryarray=['BTM', 'LOW', 'SAFE', 'HIGH', 'WIN']
    )

    fig.update_xaxes(
        dtick=1
    )
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)