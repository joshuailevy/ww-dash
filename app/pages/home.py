import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.P(['This is a simple resource to query for specific mutations and lineages across SRA wastewater samples.',html.Br(),
    'All data is publicly available and analyses are performed using the Freyja package.']),
    html.Div([html.Img(src=dash.get_asset_url('../assets/ncbi-logo.jpeg')),html.Img(src=dash.get_asset_url('../assets/search-logo.png'),style={'height':'25%', 'width':'25%'}),
        ]),
    ], style = {'textAlign': 'center'})