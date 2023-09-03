import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.subplots
import plotly.graph_objects as go

pd.set_option('display.max_rows', None)

class list_biblio100cols():

    def __init__(self,filename='database/basecol/data_website/all_col.csv'):
        colFrance=pd.read_csv(filename,delimiter=';')
        colFrance[colFrance.columns[0]]=colFrance[colFrance.columns[0]].str.replace(' ', '')
        colFrance[colFrance.columns[2]]=np.float64(colFrance[colFrance.columns[2]])
        colFrance[colFrance.columns[4]]=np.float64(colFrance[colFrance.columns[4]])
        colFrance[colFrance.columns[5]]=np.float64(colFrance[colFrance.columns[5]])
        self.database=colFrance

        
    def filter_name(self,str_r,dep=None,alt=None,print_res=True):

        id=pd.Series(list(self.database[self.database.columns[1]])).str.contains(str_r,case=False)
        
        if alt is not None:
            id2=pd.Series(self.database[self.database.columns[2]]==alt)
            id = id*id2
        if dep is not None:
            id2=pd.Series(self.database[self.database.columns[0]].str.contains(dep,case=False))
            id = id*id2
        if print_res:
            print('Nothing')
        return id

    def plot_map(self,id,ww=1000,gpx=None):
        
        index=self.database.columns

        fig = px.scatter_mapbox(self.database.loc[id], lat=index[5], lon=index[4], hover_name=index[1], hover_data=[index[0], index[2]],
                                color_discrete_sequence=["blue"], zoom=7,width=0.8*ww,height=0.3*ww)
        if gpx is not None:
            index2=gpx.columns
            fig2 = px.line_mapbox(gpx, lat=index2[1], lon=index2[2], color_discrete_sequence=["red"],width=0.8*ww,height=0.3*ww)
            fig = go.Figure(data = fig2.data + fig.data)
            fig.update_mapboxes(center={"lat":gpx['latitude'].mean(),"lon":gpx['longitude'].mean()})
            fig.update_mapboxes(zoom=9)
            
        fig.update_layout(mapbox_style="open-street-map")
        return fig
