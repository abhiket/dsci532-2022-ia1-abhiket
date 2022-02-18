from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd 

# Read in global data
url = "https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv"
gm = pd.read_csv(url, parse_dates=['year']) 
gm1962 = gm.query('year == 1962')

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='life_expectancy',  
        options=[{'label': col, 'value': col} for col in gm1962.columns])])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'))
def plot_altair(xcol):
    chart = alt.Chart(gm1962).mark_point().encode(
        x=xcol,
        y='life_expectancy',
        tooltip='region').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)