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
        dcc.Input(id='my-input3', value='SRR25665961', type='text', debounce = True)
    ]),
    html.Br(),
    html.Div([
    html.Div(id='my-output3'),
    html.Div(dcc.Graph(id='barplot'),style={
                            "width": "68%",
                            "height": "800px",
                            "display": "inline-block",
                            "padding-top": "5px",
                            "padding-left": "1px",
                            "overflow": "hidden"}),

],style = {'textAlign': 'center',
           'marginLeft': 'auto',
           'marginRight': 'auto'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})

@callback(
    Output(component_id='my-output3', component_property='children'),
    Input(component_id='my-input3', component_property='value')
)
def update_output_div(input_value):
    if input_value in dat.keys():
        return f'Found sample: {input_value}'
    else:
        return ''


@callback(
    Output('barplot', 'figure'),
    Input('my-input3', component_property = 'value'))
def update_figure(input_value):
    df0 = pd.Series(dat[input_value]).to_frame().T
    cols = df0.columns
    df0['Sample'] = input_value
    fig = px.bar(df0,x='Sample',y=cols,title='Lineage prevalence estimates (Freyja)', width = 600,height=600)

    fig.update_layout(transition_duration=100)

    return fig
