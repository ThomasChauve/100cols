import streamlit as st
from pathlib import Path
import time
import numpy as np
import pickle
import io
import datetime

st.set_page_config(page_title="Exporter le rapport", page_icon="📤")

st.markdown("Cette outil permet d'exporter un rapport pour envoyer au club des 100 cols.")
st.warning("Cela ne fait pas une sauvegarde de vos données. Pour cela utilisé les bouttons *Téléchargement* à gauche.", icon="⚠️")

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


st.title('Export des cols')

def send_pdf(adr):
    with open(adr, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    return PDFbyte


if len(user_list)==0:
    st.warning("Pas d'utilisateur enregistré")
else:
    o_nom=st.text_input('Nom et Prénom',value=st.session_state['data_list'][st.session_state['id_u']].name,label_visibility="visible")
    o_id=st.number_input('id club',value=st.session_state['data_list'][st.session_state['id_u']].id100col, label_visibility="visible",min_value=int(0))
    o_date=st.date_input('Date limite', label_visibility="visible")

    if st.button('Générer rapport'):
        st.session_state['data_list'][st.session_state['id_u']].export_pdf(o_nom,o_id,o_date,st.session_state['data_list'][st.session_state['id_u']].pseudo+str(o_date.year))
        st.success('Export réussit !', icon="✅")
        st.download_button('Télécharger le rapport de '+ st.session_state['data_list'][st.session_state['id_u']].pseudo,send_pdf(st.session_state['data_list'][st.session_state['id_u']].pseudo+str(o_date.year)+'.pdf'),file_name=st.session_state['data_list'][st.session_state['id_u']].pseudo+str(datetime.date.today())+'.pdf',key='er')

