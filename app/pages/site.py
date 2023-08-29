import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import pickle
import plotly.graph_objects as go

dash.register_page(__name__)

dat = pickle.load(open("samples_deconv_dict.pkl",'rb'))
df_meta = pd.read_csv('wastewater_ncbi.csv',index_col=0)


layout = html.Div([
    html.H6("Enter a sampling site of interest:"),
    html.Div([
        dcc.Input(id='site', value='OH0025003', type='text', debounce = True,style={'width':'400px','textAlign': 'center'})
    ],style={'textAlign': 'center','marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    html.Div([
    html.P('Note: Freyja results will only be shown for samples with >60 percent genome coverage.'),
    html.Div(dcc.Graph(id='barplot-site',config={'displayModeBar': False},style={'width': '1200px', 'height': '500px'}),style={
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
           'marginRight': 'auto'})
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
    samples = [iv0 for iv0 in meta_loc.index if iv0 in dat.keys()]
    meta_loc = meta_loc.loc[samples]
    df0 = pd.concat([pd.Series(dat[iv0],name=iv0).to_frame() for iv0 in samples],axis=1).T
    df0 = df0.drop(columns=['Other']) #account for rounding/thresholding
    df0['Other'] = (1.- df0.sum(axis=1)) #account for rounding/thresholding
    cols = df0.columns
    # print(df0)
    df0['Sample'] = meta_loc['collection_date']
    df0 = df0.fillna(0).groupby(by='Sample').mean().reset_index()
    print(df0)
    fig = px.bar(df0,x='Sample',y=cols, width=1200, height=500,color_discrete_sequence=px.colors.qualitative.Dark24,
)
    # fig.add_trace(go.scatter(df0,x='Sample',y=cols))
    # fig.update_traces(marker_line_width=1.5)
    fig.update_layout(transition_duration=100,title_text='Lineage prevalence estimates (Freyja)',
                      title_x=0.5,showlegend=False, yaxis_title='Lineage prevalence',xaxis_title='')
    # fig.update_xaxes(tickvals=meta_loc['collection_date'])# meta_loc['collection_date'])

    meta_loc = meta_loc.loc[:,['collection_date','geo_loc_name','ww_population','site id']].reset_index()
    cols = list(meta_loc.columns)
    cols[0] = 'Sample'
    meta_loc.columns = cols
    return fig, meta_loc.to_dict('records')



