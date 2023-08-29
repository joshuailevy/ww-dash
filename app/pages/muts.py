import dash
from dash import dcc, html, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px


dash.register_page(__name__)

filepath = "testData.csv"
df = pd.read_csv(filepath)
muts = df['mutName']
df = df.set_index(['mutName','sample']).drop_duplicates()

df_meta = pd.read_csv('wastewater_ncbi.csv',index_col=0)



layout = html.Div([
    html.H6("Enter a mutation of interest:"),
    html.Div([
        dcc.Input(id='my-input', value='G21608+TCATGCCGCTGT', type='text', debounce = True,style={'width':'400px','textAlign': 'center'})
    ],style={'textAlign': 'center','marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    html.Div([
    dcc.Graph(id="graph",config={'displayModeBar': False}),
    dash_table.DataTable(
        id='datatable-paging-page-count',
        page_current=0,
        page_size=20,
        # page_action='custom',
        # filter_action="native",
        # filter_options={"placeholder_text": "Filter column..."},
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '60%','textAlign': 'center', 'maxWidth': '1000px', 'marginLeft': 'auto', 'marginRight': 'auto'},
        style_cell={'textAlign': 'center','font-size':'14px'}
    ),
],style = {'textAlign': 'center',
           'marginLeft': 'auto',
           'marginRight': 'auto'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})


@callback(
    Output('datatable-paging-page-count', 'data'),
    Output("graph", "figure"), 
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

        if all([di in df_meta.index for di in dat.index]):
            meta = df_meta.loc[dat.index,['collection_date','geo_loc_name','ww_population','site id']]
        else:
            print("Samples missing from metadata file!")
            dat = dat.loc[[di for di in dat.index if di in df_meta.index]]
            meta = df_meta.loc[dat.index,['collection_date','geo_loc_name','ww_population', 'site id']]
        dfCombo = pd.concat((dat,meta),axis=1).sort_values(by='collection_date',ascending=False)
        countries = dfCombo['geo_loc_name'].apply(lambda x:x.split(':')[0])
        dfCombo = dfCombo.rename(columns = {"ALT_FREQ": "FREQUENCY",'ALT_DP':'DEPTH','geo_loc_name':'LOCATION','ww_population':'POPULATION','collection_date':'Collection date'})
        dfCombo["FREQUENCY"] = dfCombo["FREQUENCY"].round(2)
        locs = countries.value_counts()
        fig = px.choropleth(locations=locs.index,locationmode='country names',color=locs,color_continuous_scale='YlOrRd',projection='winkel tripel')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},xaxis={'fixedrange':True},yaxis={'fixedrange':True},dragmode=False,hovermode="x unified")
        fig.update_traces(hovertemplate=None)
        fig.update(layout_coloraxis_showscale=False) 
        return dfCombo.reset_index().to_dict('records'), fig
