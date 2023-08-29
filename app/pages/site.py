import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import pickle

dash.register_page(__name__)

dat = pickle.load(open("samples_deconv_dict.pkl",'rb'))
df_meta = pd.read_csv('wastewater_ncbi.csv',index_col=0)


layout = html.Div([
    html.H6("Enter a sampling site of interest:"),
    html.Div([
        dcc.Input(id='site', value='HibzTsFeNi4e', type='text', debounce = True,style={'width':'400px','textAlign': 'center'})
    ],style={'textAlign': 'center','marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    html.Div([
    html.P('Note: Freyja results will only be shown for samples with >60 percent genome coverage.'),
    html.Div(dcc.Graph(id='barplot-site',config={'displayModeBar': False}),style={
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
    dash_table.DataTable(
        id='datatable-paging-page-count4',
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
           'marginRight': 'auto',
           'maxWidth': '1000px'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})

@callback(
    Output('barplot-site', 'figure'),
    Output('datatable-paging-page-count4', 'data'),
    Input('site', component_property = 'value'))
def update_figure(input_value):
    input_value = input_value.replace(' ','')
    meta_loc = df_meta[df_meta['site id']==input_value]
    print(meta_loc)
    print(meta_loc['collection_date'])
    # meta_loc = meta_loc[meta_loc.index.isin(dat.keys())]
    meta_loc = meta_loc.sort_values(by='collection_date')
    samples = meta_loc.index
    print(samples)
    df0 = pd.concat([pd.Series(dat[iv0],name=iv0).to_frame() for iv0 in samples],axis=1).T
    cols = df0.columns
    print(df0)
    df0 = df0.drop(columns=['Other']) #account for rounding/thresholding
    df0['Other'] = (1.- df0.sum(axis=1)) #account for rounding/thresholding
    # print(df0)
    df0['Sample'] = meta_loc['collection_date']
    print(df0)
    fig = px.bar(df0,x='Sample',y=df0.columns, width = 600,height=600)
    fig.update_layout(transition_duration=100,title_text='Lineage prevalence estimates (Freyja)',
                      title_x=0.5,showlegend=False, yaxis_title='Lineage prevalence')
    fig.update_xaxes(tickvals=meta_loc['collection_date'])

    meta_loc = meta_loc.loc[:,['collection_date','geo_loc_name','ww_population','site id']].reset_index()
    cols = list(meta_loc.columns)
    cols[0] = 'Sample'
    meta_loc.columns = cols
    return fig, meta_loc.to_dict('records')



