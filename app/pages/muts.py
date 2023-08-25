import dash
from dash import dcc, html, Input, Output, callback, dash_table
import pandas as pd

dash.register_page(__name__)

filepath = "testData.csv"
df = pd.read_csv(filepath)
muts = df['mutName']
df = df.set_index(['mutName','sample']).drop_duplicates()

df_meta = pd.read_csv('wastewater_ncbi.csv',index_col=0)
PAGE_SIZE = 50


layout = html.Div([
    html.H6("Enter a mutation of interest:"),
    html.Div([
        dcc.Input(id='my-input', value='G21608+TCATGCCGCTGT', type='text', debounce = True)
    ]),
    html.Br(),
    html.Div([
    dash_table.DataTable(
        id='datatable-paging-page-count',
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
    Output('datatable-paging-page-count', 'data'),
    Input(component_id='my-input', component_property='value')
    )
def update_table(input_value):
    input_value = input_value.replace(' ','')
    if all([iV in df.index for iV in input_value.split(',')]):
        dat = pd.DataFrame()
        for iV in input_value.split(','):
            grp = df.loc[pd.IndexSlice[iV,:]]
            grp.insert(0,'mutation',iV)
            dat = pd.concat((dat,grp))
        if len(input_value.split(','))>1:
            dat = dat.loc[dat.index.value_counts()==len(input_value.split(','))]

        meta = df_meta.loc[dat.index,['collection_date','geo_loc_name','ww_population']]
        dfCombo = pd.concat((dat,meta),axis=1).sort_values(by='collection_date',ascending=False)
        return dfCombo.reset_index().to_dict('records')
