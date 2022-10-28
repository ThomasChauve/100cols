import streamlit as st
import time
import numpy as np
import libpy_100c.libpy_100c as lc
import libpy_100c.lib_biblio100cols as lb100
import pickle
import io
import datetime

st.set_page_config(page_title="Supprimer un col", page_icon="➖")

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


width = 1980

if len(user_list)==0:
    st.title('Supprimer un col')
    st.warning("Pas d'utilisateur enregistré")
else:
    st.title('Supprimer un col à '+option)
    st.header('Recherche')

    f_id=st.text_input('Code',label_visibility="visible")
    f_nom=st.text_input('Nom',label_visibility="visible")

    id=st.session_state['data_list'][st.session_state['id_u']].filter_name(f_nom,dep=f_id,alt=None,date=None,print_res=False)
    
    st.dataframe(st.session_state['data_list'][st.session_state['id_u']].cols.loc[id])
    
    del_code = st.selectbox('Col à supprimer',st.session_state['data_list'][st.session_state['id_u']].cols.loc[id])

    
    if st.button('Supprimer'):        
        st.session_state['data_list'][st.session_state['id_u']].del_pass(del_code)
        
        st.success('Col '+del_code+' supprimé', icon="✅")
