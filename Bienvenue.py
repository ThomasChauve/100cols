import streamlit as st
import pickle
import libpy_100c.libpy_100c as lc
import libpy_100c.lib_biblio100cols as lb100
import numpy as np
import pandas as pd
import io
import datetime


st.set_page_config(
    page_title="Club des 100 cols",
    page_icon="👋",
)

st.title('Bienvenue dans votre gestionaire de cols')

st.warning('Une fois les modifications réalisées n'oublier pas de télécharger vos données mise à jour.')


st.header('Charger les données')

if 'id_u' not in st.session_state:
    st.session_state['id_u'] = 0

if 'data_list' not in st.session_state:
    st.session_state['data_list']=[]

def data_load(file):
    dd=pickle.load(file)
    data=lc.list100cols()
    data.__dict__.update(dd)
    return data

uploaded_file=st.file_uploader('Charger fichier ".100cols"',accept_multiple_files=True, type='100cols', label_visibility="visible")
if uploaded_file is not None:
    for f in uploaded_file:
        st.session_state['data_list'].append(data_load(f))
        

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
            st.download_button('Télécharger les donnée de '+ data.pseudo,pickle_model(data),file_name=data.pseudo+str(datetime.date.today())+'.100cols',key='uk-1'+str(k))
            k+=1


