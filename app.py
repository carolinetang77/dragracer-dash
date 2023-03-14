import altair as alt
import pandas as pd
from dash import dash, dcc, html, Input, Output

# import data
dr_data = pd.read_csv('data/drag.csv', index_col=0)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Drag Race Visualizer'),
    dcc.Dropdown(
        id = 'season', 
        options = sorted(dr_data['season'].unique()),
        value = 'S01'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)