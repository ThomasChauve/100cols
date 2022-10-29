import streamlit as st
import time
import numpy as np
import pickle
from datetime import datetime
import io
import datetime

st.set_page_config(page_title="Statistique des cols",layout="wide", page_icon="📊")

if 'id_u' not in st.session_state:
    st.session_state['id_u'] = 0

if 'data_list' not in st.session_state:
    st.session_state['data_list']=[]

user_list=[]
for du in st.session_state['data_list']:
    user_list.append(du.pseudo)

def pickle_model(model):
    f = io.BytesIO()
    pickle.dump(model.__dict__, f)
    return f 

if len(user_list)!=0:
    with st.sidebar:
        option = st.selectbox('Utilisateur',user_list,index=st.session_state['id_u'],key='u1')
        st.session_state['id_u']=user_list.index(option)
        k=0
        for data in st.session_state['data_list']:
            st.download_button('Télécharger les données de '+ data.pseudo,pickle_model(data),file_name=data.pseudo+'.100cols',key='uk-1'+str(k))
            k+=1

width = 1980

if len(user_list)==0:
    st.title('Statistique des cols')
    st.warning("Pas d'utilisateur enregistré")
else:
    st.title("Statistique des cols de "+option)
    if len(st.session_state['data_list'][st.session_state['id_u']].cols)==0:
        st.warning(st.session_state['data_list'][st.session_state['id_u']].name+" n'a pas encore de col enregistré.")
    else:
        st.write(option+' a fait '+str(len(st.session_state['data_list'][st.session_state['id_u']].cols))+' cols, dont '+str(np.sum(st.session_state['data_list'][st.session_state['id_u']].cols.Altitude>2000))+' de plus de 2000 m.')

        fig_hist=st.session_state['data_list'][st.session_state['id_u']].plot_histogram()
        fig_cum=st.session_state['data_list'][st.session_state['id_u']].plot_evolution_col()
        fig_map=st.session_state['data_list'][st.session_state['id_u']].plot_map(ww=width)
        fig_pays=st.session_state['data_list'][st.session_state['id_u']].plot_pays()
        fig_dep=st.session_state['data_list'][st.session_state['id_u']].plot_dep()


        st.plotly_chart(fig_map, use_container_width=True, sharing="streamlit")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig_hist, use_container_width=True, sharing="streamlit")
        with col2:
            st.plotly_chart(fig_cum, use_container_width=True, sharing="streamlit")
        with col1:
            st.plotly_chart(fig_pays, use_container_width=True, sharing="streamlit")
        with col2:
            st.plotly_chart(fig_dep, use_container_width=True, sharing="streamlit")
