from django.shortcuts import render

# Create your views here.
from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

app.layout = html.Div([
    dcc.Input(id='input', type='text', value='Django + Dash'),
    html.Div(id='output')
])

@app.callback(
    Output('output', 'children'),
    Input('input', 'value')
)
def update_output(value):
    return f'Has escrito: {value}'
