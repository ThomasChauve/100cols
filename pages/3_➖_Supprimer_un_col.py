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
        k=0
        for data in st.session_state['data_list']:
            st.download_button('Télécharger les données de '+ data.pseudo,pickle_model(data),file_name=data.pseudo+str(datetime.date.today())+'.100cols',key='uk-1'+str(k))
            k+=1

width = 1980

if len(user_list)==0:
    st.title('Supprimer un col')
    st.warning("Pas d'utilisateur enregistré")
else:
    st.title('Supprimer un col à '+option)
    st.header('Recherche')

    f_id=st.text_input('Code',label_visibility="visible")
    f_nom=st.text_input('Nom',label_visibility="visible")
    f_alt=st.number_input('Altitude', label_visibility="visible",min_value=int(0))

    if f_alt==0:
        aa=None
    else:
        aa=f_alt


    id=st.session_state['data_list'][st.session_state['id_u']].filter_name(fu_nom,dep=fu_id,alt=fu_alt,date=fu_date,print_res=False)
    del_code = st.selectbox('Col à supprimer',st.session_state['data_list'][st.session_state['id_u']].cols.loc[id])

    
    if st.button('Supprimer'):
        index=list(st.session_state['data_list'][st.session_state['id_u']].cols[colAll.database.columns[0]]).index(del_code)
        
        st.session_state['data_list'][st.session_state['id_u']].del_pass(index)
        
        st.success('Col '+del_code+' supprimé', icon="✅")