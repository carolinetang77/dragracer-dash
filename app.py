from dash import dash, html

app = dash.Dash(__name__)

app.layout = html.Div('I am alive!!')

if __name__ == '__main__':
    app.run_server(debug=True)