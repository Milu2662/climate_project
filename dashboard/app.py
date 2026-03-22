import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

df = pd.read_parquet("datalake_silver/data.parquet")

app = dash.Dash(__name__)

fig = px.histogram(df, x="label", title="Sentiment Distribution")

app.layout = html.Div([
    html.H1("Climate Sentiment Dashboard"),

    dcc.Graph(figure=fig)
])

app.run(debug=True)