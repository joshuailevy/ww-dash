import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from navbar import create_navbar


FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"

NAVBAR = create_navbar()

app = Dash(__name__, 
    external_stylesheets=[
        dbc.themes.LUX,  # Dash Themes CSS
        FA621,  # Font Awesome Icons CSS
    ],
    use_pages=True)

app.layout = dcc.Loading(  # <- Wrap App with Loading Component
    id='loading_page_content',
    children = [
        html.Div([
        NAVBAR,
        dash.page_container
        ])
        ],
    color='primary',
    fullscreen=True
    )

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)

