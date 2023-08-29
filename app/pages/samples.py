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
        dcc.Input(id='my-input3', value='SRR25657365,SRR25726416', type='text', debounce = True,style={'width':'400px','textAlign': 'center'})
    ],style={'textAlign': 'center','marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    html.Div([
    html.Div(dcc.Graph(id='barplot',config={'displayModeBar': False}),style={
                            # "width": "68%",
                            # "height": "800px",
                            "display": "inline-block",
                            "padding-top": "5px",
                            "padding-left": "1px",
                            "overflow": "hidden",
                            "textAlign": "center",
                            'marginLeft': 'auto',
                            'marginRight': 'auto',
                            }),
    dash_table.DataTable(
        id='datatable-paging-page-count3',
        page_current=0,
        page_size=20,
        # page_action='custom',
        # filter_action="native",
        # filter_options={"placeholder_text": "Filter column..."},
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '60%','textAlign': 'center', 'maxWidth': '1000px', 'marginLeft': 'auto', 'marginRight': 'auto'},
        style_cell={'textAlign': 'center','font-size':'14px'}
    )
    ],style = {'textAlign': 'center',
           'marginLeft': 'auto',
           'marginRight': 'auto'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})

@callback(
    Output('barplot', 'figure'),
    Input('my-input3', component_property = 'value'))
def update_figure(input_value):
    input_value = input_value.replace(' ','')
    # print(dat[input_value.split(',')[0]])
    df0 = pd.concat([pd.Series(dat[iv0],name=iv0).to_frame() for iv0 in input_value.split(',')],axis=1).T
    cols = df0.columns
    df0 = df0.drop(columns=['Other']) #account for rounding/thresholding
    df0['Other'] = (1.- df0.sum(axis=1)) #account for rounding/thresholding
    print(df0)
    df0['Sample'] = input_value.split(',')
    fig = px.bar(df0,x='Sample',y=df0.columns, width = 600,height=600)
    fig.update_layout(transition_duration=100,title_text='Lineage prevalence estimates (Freyja)',
                      title_x=0.5,showlegend=False, yaxis_title='Lineage prevalence')

    return fig


@callback(
    Output('datatable-paging-page-count3', 'data'),
    Input(component_id='my-input3', component_property='value')
    )
def update_table(input_value):
    input_value = input_value.replace(' ','')
    iVs = input_value.split(',')
    if all([iV in df_meta.index for iV in iVs]):
        meta = df_meta.loc[iVs,['collection_date','geo_loc_name','ww_population','site id']].reset_index()
        cols = list(meta.columns)
        cols[0] = 'Sample'
        meta.columns = cols
    else:
        print("Samples missing from metadata file!")

    return meta.to_dict('records')

