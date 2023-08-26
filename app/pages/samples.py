import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import pickle

dash.register_page(__name__)

dat = pickle.load(open("samples_deconv_dict.pkl",'rb'))
df_meta = pd.read_csv('wastewater_ncbi.csv',index_col=0)


layout = html.Div([
    html.H6("Enter a sample of interest:"),
    html.Div([
        dcc.Input(id='my-input3', value='SRR25657365', type='text', debounce = True)
    ]),
    html.Br(),
    html.Div([
    html.Div(dcc.Graph(id='barplot',config={'displayModeBar': False}),style={
                            "width": "68%",
                            "height": "800px",
                            "display": "inline-block",
                            "padding-top": "5px",
                            "padding-left": "1px",
                            "overflow": "hidden",
                            "textAlign": "center",
                            'marginLeft': 'auto',
                            'marginRight': 'auto',
                            'minWidth': '60%', 'maxWidth': '1000px'}),

],style = {'textAlign': 'center',
           'marginLeft': 'auto',
           'marginRight': 'auto',
           'maxWidth': '1000px'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})

@callback(
    Output('barplot', 'figure'),
    Input('my-input3', component_property = 'value'))
def update_figure(input_value):
    df0 = pd.Series(dat[input_value]).to_frame().T
    cols = df0.columns
    df0['Sample'] = input_value
    fig = px.bar(df0,x='Sample',y=cols, width = 600,height=600)
    fig.update_layout(transition_duration=100,title_text='Lineage prevalence estimates (Freyja)',
                      title_x=0.5,showlegend=False, yaxis_title='Lineage prevalence')

    return fig
