import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.subplots

pd.set_option('display.max_rows', None)

class list_biblio100cols():

    def __init__(self,filename='database/basecol/data_website/all_col.csv'):
        colFrance=pd.read_csv(filename,delimiter=';')
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

    def plot_map(self,id,ww=1000):
        
        index=self.database.columns

        fig = px.scatter_mapbox(self.database.loc[id], lat=index[5], lon=index[4], hover_name=index[1], hover_data=[index[0], index[2]],
                                color_discrete_sequence=["blue"], zoom=4,width=0.8*ww,height=0.3*ww)
        fig.update_layout(mapbox_style="open-street-map")
        #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
