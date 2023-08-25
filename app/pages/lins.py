import dash
from dash import dcc, html, Input, Output, callback, dash_table
import pandas as pd
import pickle

dash.register_page(__name__)

dat = pickle.load(open("lineage_dict.pkl",'rb'))
df_meta = pd.read_csv('wastewater_ncbi.csv',index_col=0)


layout = html.Div([
    html.H6("Enter a lineage of interest:"),
    html.Div([
        dcc.Input(id='my-input2', value='XBB.1.9.1', type='text', debounce = True)
    ]),
    html.Br(),
    html.Div([
    html.Div(id='my-output2'),
    dash_table.DataTable(
        id='datatable-paging-page-count2',
        # page_current=0,
        # page_size=PAGE_SIZE,
        # page_action='custom',
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '60%','textAlign': 'center', 'maxWidth': '1000px', 'marginLeft': 'auto', 'marginRight': 'auto'},
        style_cell={'textAlign': 'center'}
    ),
],style = {'textAlign': 'center',
           'marginLeft': 'auto',
           'marginRight': 'auto'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})

@callback(
    Output(component_id='my-output2', component_property='children'),
    Input(component_id='my-input2', component_property='value')
)
def update_output_div(input_value):
    if input_value in dat.keys():
        return f'Found lineage: {input_value}'
    else:
        return ''

@callback(
    Output('datatable-paging-page-count2', 'data'),
    Input(component_id='my-input2', component_property='value')
    )
def update_table(input_value):
    if input_value in dat.keys():
        df0 = pd.DataFrame.from_dict(dat[input_value],orient='index',columns=['ALT_FREQ'])
        meta = df_meta.loc[df0.index,['collection_date','geo_loc_name','ww_population']]
        dfCombo = pd.concat((df0,meta),axis=1).sort_values(by='collection_date',ascending=False).reset_index()
        cols = list(dfCombo.columns)
        cols[0] = 'SRA Accession'
        dfCombo.columns = cols
        return dfCombo.to_dict('records')
