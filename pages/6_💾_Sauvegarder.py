import streamlit as st
from pathlib import Path
import numpy as np
import pickle
import io
import datetime

st.set_page_config(page_title="Sauvegarder", page_icon="💾")

st.session_state['d_date']=datetime.date.today()
st.session_state['filter_gpx']=False
st.session_state['id_f']=None
st.session_state['up_gpx']=None

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


st.title('Sauvegarder les cols')
st.header('Fichier .100cols ')
k=0
for data in st.session_state['data_list']:
  st.download_button('Télécharger les données .100cols de '+ data.pseudo,pickle_model(data),file_name=data.pseudo+'.100cols',key='uk-1'+str(k))
  k+=1
 
st.header('Fichier .csv')
st.markdown("Un fichier .csv peut etre ouvert avec votre tableur favoris (Libre Office Calc, Excel, ...)")
st.warning('Ce fichier ne permet pas de recharger les données dans ce site internet',icon="⚠️")
k=0
for data in st.session_state['data_list']:
  data.cols.to_csv('tmp'+str(k)+'.csv',sep=';')
  st.download_button('Télécharger les données .csv de '+ data.pseudo,data=Path('tmp'+str(k)+'.csv').read_text(),file_name=data.pseudo+'.csv',key='uke-1'+str(k))
  k+=1
  

