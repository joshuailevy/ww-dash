from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Mutations", href='/muts'),
                    dbc.DropdownMenuItem("Lineages", href='/lins'),
                    dbc.DropdownMenuItem("Samples", href='/samples'),
                    dbc.DropdownMenuItem("Site", href='/site'),
                ],
            ),
        ],
        brand='Wastewater genomic surveillance, enabled by NCBI SRA',
        brand_href="/",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar