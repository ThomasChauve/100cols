import streamlit as st
import libpy_100c.libpy_100c as lc
import time
import numpy as np
import pickle
import io
import datetime

st.set_page_config(page_title="Gestion des utilisateurs", page_icon="👥")

if 'id_u' not in st.session_state:
    st.session_state['id_u'] = 0
if 'data_list' not in st.session_state:
    st.session_state['data_list']=[]

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


st.title('Gestion des utilisateurs')

add_user, edit_profil = st.tabs(['Ajouter un utilisateur', 'Editer un profil'])

with add_user:
    o_pseudo=st.text_input('Pseudo',label_visibility="visible",key='au_ps')
    o_nom=st.text_input('Nom et Prénom',label_visibility="visible",key='au_n')
    o_id=st.number_input('id club', label_visibility="visible",min_value=int(0),key='au_id')

    if st.button('Ajouter utilisateur'):
        st.session_state['data_list'].append(lc.list100cols(id100col=o_id,name=o_nom,pseudo=o_pseudo))
        st.success('Ajout de '+ o_nom +' réussit !', icon="✅")

with edit_profil:
    if len(user_list)==0:
        st.warning("Pas d'utilisateur enregistré")
    else:
        du=st.session_state['data_list'][st.session_state['id_u']]
        o_pseudo=st.text_input('Pseudo',value=du.pseudo,label_visibility="visible",key='eu_ps')
        o_nom=st.text_input('Nom et Prénom',value=du.name,label_visibility="visible",key='eu_n')
        o_id=st.number_input('id club', value=du.id100col, label_visibility="visible",min_value=int(0),key='eu_id')

        if st.button('Mettre à jour'):
            st.session_state['data_list'][st.session_state['id_u']].pseudo=o_pseudo
            st.session_state['data_list'][st.session_state['id_u']].name=o_nom
            st.session_state['data_list'][st.session_state['id_u']].id100col=o_id
            st.success('Mise à jour de '+ o_nom +' réussit !', icon="✅")
