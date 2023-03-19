import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash, dcc, dash_table, html, Input, Output, State
from dash_bootstrap_templates import load_figure_template

# url for themes
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template('pulse')

# import data 
dr_data = pd.read_csv('../data/drag.csv', index_col=0)

# remove all episodes where queens didn't compete
dr_data = dr_data[dr_data['participant'].apply(lambda x: x == 1)]

# dob table
dob = (
    dr_data[['season', 'rank', 'contestant', 'outcome']]
    .groupby(['season', 'rank', 'contestant'])
    .value_counts(['outcome'])
    .reset_index(name = 'count')
    .pivot(index = ['season', 'rank', 'contestant'], columns = 'outcome', values = 'count')
    .reset_index()
    .fillna(0)
)[['season', 'rank', 'contestant', 'WIN', 'HIGH', 'SAFE', 'LOW', 'BTM']]
dob['dob'] = 2 * dob['WIN'] + dob['HIGH'] - dob['LOW'] - 2 * dob['BTM']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE, dbc_css])

server = app.server

app.layout = dbc.Container([
    html.H1('Drag Race Visualizer'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody([
                        html.P("""
                            This data was originally obtained from data scraped from the RuPaul's
                            Drag Race wiki. The bar graph is based on the unofficial Dusted or Busted score, 
                            which offers a numerical representation of a queen's performance
                            on their respective season, as follows:
                        """),
                        html.Table([
                            html.Tr([html.Th('Rank'), html.Th('Score')]),
                            html.Tr([html.Td('Win'), html.Td('+2')]),
                            html.Tr([html.Td('High'), html.Td('+1')]),
                            html.Tr([html.Td('Safe'), html.Td('+0')]),
                            html.Tr([html.Td('Low'), html.Td('-1')]),
                            html.Tr([html.Td('Bottom'), html.Td('-2')]),
                        ])
                    ])
                ), 
                id = 'helptext', 
                is_open = False
            ),
            dbc.Button(
                "Show Info",
                id="collapse-button",
                color="info",
                size="sm"
            ),
            html.Br(),
            html.Br(),
            html.Label('Seasons:'),
            dcc.Dropdown(
                id = 'season', 
                options = sorted(dr_data['season'].unique()),
                multi=True,
                placeholder='Select one or more seasons'
            ),
            html.Br(),
            html.Label('Queens:'),
            dcc.Dropdown(
                id = 'queen', 
                options = sorted(dr_data['contestant'].unique()),
                value = dr_data.query("winner == 1")['contestant'].unique(),
                multi=True,
                placeholder='Select one or more queens'
            )
        ], md = 2),
        dbc.Col([
            html.H3('Scores'),
            dcc.Graph(
                id = 'performance'
            ),
        ], md = 5),
        dbc.Col([
            html.H3('Performance Summary'),
            dash_table.DataTable(
                id='table', 
                columns=[{"name": col, "id": col} for col in dob.columns],
                sort_action="native",
                page_size=15,
                fixed_rows={'headers': True},
                style_cell={'textAlign': 'left'},
                style_cell_conditional=[
                    {'if': {'column_id': 'contestant'},
                    'width': '30%'},
                    {'if': {'column_id': ['season']},
                    'width': '10%'},
                    {'if': {'column_id': ['dob', 'rank', 'BTM', 'HIGH', 'LOW', 'SAFE', 'WIN']},
                    'width': '7%'},
                ]
            )
        ], md = 5)
    ])
], className = "dbc", fluid = True)

@app.callback(
    Output("helptext", "is_open"),
    Output("collapse-button", "children"),
    Input("collapse-button", "n_clicks"),
    State("helptext", "is_open"),
)
def toggle_collapse(n, is_open):
    button_text = "Show Info"
    if n:
        if is_open:
            button_text = "Show Info"
        else:
            button_text = "Hide Info"
        return not is_open, button_text
    return is_open, button_text

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
        values = None
    else:
        options = sorted(dr_data['contestant'].unique())
        if queens is None or len(queens) == 0:
            values = dr_data.query("winner == 1")['contestant'].unique()
        else:
            values = queens
    return options, values

@app.callback(
    Output('performance', 'figure'),
    Output('table', 'data'),
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
        text = 'dob',
        color_continuous_scale='Plotly3',
        range_color=[-10, 15],
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
    
    fig.update_traces(textangle=0, textposition="outside")

    fig.update_layout(
        coloraxis_showscale = False,
        margin=dict(l=10, r=10, t=30, b=0)
    )
    return fig, filtered.sort_values(['rank', 'dob'], ascending = [True, False]).to_dict('records')
    

if __name__ == '__main__':
    app.run_server(debug=True)