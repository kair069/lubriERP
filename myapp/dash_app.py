from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

# Define la aplicación Dash
app = DjangoDash('SimpleExample')

# Layout de la aplicación
app.layout = html.Div([
    dcc.Input(id='input', type='text', value='Django + Dash'),
    html.Div(id='output')
])

# Callback para actualizar el texto
@app.callback(
    Output('output', 'children'),
    Input('input', 'value')
)
def update_output(value):
    return f'Has escrito: {value}'
