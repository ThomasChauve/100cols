import streamlit as st
import numpy as np
import pickle
import io
import datetime

st.set_page_config(page_title="Liste des cols", page_icon="📝")

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
        k=0
        for data in st.session_state['data_list']:
            st.download_button('Télécharger les données de '+ data.pseudo,pickle_model(data),file_name=data.pseudo+'.100cols',key='uk-1'+str(k))
            k+=1

if len(user_list)==0:
    st.title("Liste des cols ")
    st.warning("Pas d'utilisateur enregistré")
else:
    st.title("Nettoyage des cols de "+ option)

    st.markdown('- 3 septembre 2023 : Enlever les espaces de Code !')

if st.button('Enlever espace dans Code'):
    st.session_state['data_list'][st.session_state['id_u']].cols.Code=st.session_state['data_list'][st.session_state['id_u']].cols.Code.str.replace(' ', '')
    st.success('Espace enlevé !', icon="✅")

if st.button('Trouver et supprimer les doubles'):
    bf=len(st.session_state['data_list'][st.session_state['id_u']].cols)
    st.session_state['data_list'][st.session_state['id_u']].cols.drop_duplicates(subset=['Code'], keep='first')
    st.success('Double supprimé :'+bf-len(st.session_state['data_list'][st.session_state['id_u']].cols), icon="✅")