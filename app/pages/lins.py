import dash
from dash import dcc, html, Input, Output, callback, dash_table
import pandas as pd
import pickle
import plotly.express as px
from datetime import date


dash.register_page(__name__)

dat = pickle.load(open("lineage_dict.pkl",'rb'))
df_meta = pd.read_csv('wastewater_ncbi_ALL.csv',index_col=0)

hierarchy = pickle.load(open('hierarchy.pkl','rb'))

layout = html.Div([
    html.H6("Enter a lineage of interest:"),
    html.Div([
        dcc.Input(id='my-input2', value='B.1.1*', type='text', debounce = True,style={'width':'400px','textAlign': 'center'})
    ],style={'textAlign': 'center','marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    html.Div([
    dcc.Graph(id="graph2",config={'displayModeBar': False}),
    dash_table.DataTable(
        id='datatable-paging-page-count2',
        page_current=0,
        page_size=20,
        # page_action='custom',
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '60%','textAlign': 'center', 'maxWidth': '1000px', 'marginLeft': 'auto', 'marginRight': 'auto'},
        style_cell={'textAlign': 'center','font-size':'14px'}
    ),   html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
],style = {'textAlign': 'center',
           'marginLeft': 'auto',
           'marginRight': 'auto'})
], style = {'textAlign': 'center','marginLeft': 'auto',
           'marginRight': 'auto'})


@callback(
    Output('datatable-paging-page-count2', 'data'),
    Output("graph2", "figure"),
    Output("btn_csv", "n_clicks"),
    Input(component_id='my-input2', component_property='value')
    )
def update_table(input_value):
    if input_value.endswith('*'):
        #get all keys that start with the part before the asterisk
        prefix=input_value[0:(len(input_value)-1)]
        descendants = hierarchy[prefix]['children']
        input_vals = [key for key in dat.keys() if key in descendants]
        if len(input_vals)>0:
            df0 = pd.DataFrame()
            for iV in input_vals:
                df_ = pd.DataFrame.from_dict(dat[iV],orient='index',columns=['Frequency'])
                df0 = df0.round(2)
                df_.insert(0,'lineage',iV)
                df0 = pd.concat((df0,df_),axis=0)
            if all([di in df_meta.index for di in df0.index]):
                meta = df_meta.loc[df0.index,['collection_date','geo_loc_name','ww_population', 'site id']]
            else:
                print("Samples missing from metadata file!", len([di for di in df0.index if di not in df_meta.index]))
                df0 = df0.loc[[di for di in df0.index if di in df_meta.index]]
                meta = df_meta.loc[df0.index,['collection_date','geo_loc_name','ww_population', 'site id']]
            dfCombo = pd.concat((df0,meta),axis=1)
            dfCombo = dfCombo.reset_index()
            cols = list(dfCombo.columns)
            cols[0] = 'SRA Accession'
            dfCombo.columns = cols
            dfCombo = dfCombo.sort_values(by=['collection_date','SRA Accession'],ascending=False)
            dfCombo = dfCombo.rename(columns = {'geo_loc_name':'LOCATION','ww_population':'POPULATION','collection_date':'Collection date'})
            countries = dfCombo['LOCATION'].apply(lambda x:x.split(':')[0])
            locs = countries.value_counts()
            fig = px.choropleth(locations=locs.index,locationmode='country names',color=locs,color_continuous_scale='YlOrRd', projection='winkel tripel')
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},xaxis={'fixedrange':True},yaxis={'fixedrange':True},dragmode=False,hovermode="x unified")
            fig.update_traces(hovertemplate=None)
            fig.update(layout_coloraxis_showscale=False) 
            return dfCombo.to_dict('records'), fig, 0
    elif input_value in dat.keys():
        df0 = pd.DataFrame.from_dict(dat[input_value],orient='index',columns=['Frequency'])
        df0 = df0.round(2)
        df0.insert(0,'lineage',input_value)
        meta = df_meta.loc[df0.index,['collection_date','geo_loc_name','ww_population', 'site id']]
        dfCombo = pd.concat((df0,meta),axis=1)
        dfCombo = dfCombo.reset_index()
        cols = list(dfCombo.columns)
        cols[0] = 'SRA Accession'
        dfCombo.columns = cols
        dfCombo = dfCombo.sort_values(by=['collection_date','SRA Accession'],ascending=False)
        dfCombo = dfCombo.rename(columns = {'geo_loc_name':'LOCATION','ww_population':'POPULATION','collection_date':'Collection date'})
        countries = dfCombo['LOCATION'].apply(lambda x:x.split(':')[0])
        locs = countries.value_counts()
        fig = px.choropleth(locations=locs.index,locationmode='country names',color=locs,color_continuous_scale='YlOrRd',projection='winkel tripel')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},xaxis={'fixedrange':True},yaxis={'fixedrange':True},dragmode=False,hovermode="x unified")
        fig.update_traces(hovertemplate=None)
        fig.update(layout_coloraxis_showscale=False) 
        return dfCombo.to_dict('records'), fig, 0
    else:
        fig = px.choropleth([],locationmode='country names',projection='winkel tripel')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},xaxis={'fixedrange':True},yaxis={'fixedrange':True},dragmode=False,hovermode="x unified")
        fig.update_traces(hovertemplate=None)
        fig.update(layout_coloraxis_showscale=False) 
        return [], fig, 0

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    Input('datatable-paging-page-count2','data'),
    Input(component_id='my-input2', component_property='value'),
    prevent_initial_call=True,
)
def func(n_clicks,df_,input_value):
    if n_clicks>0 and n_clicks is not None:
        return dcc.send_data_frame(pd.DataFrame(df_).to_csv, f"{str(input_value)}_{str(date.today())}.csv")

