import streamlit as st
import pickle
import libpy_100c.libpy_100c as lc
import libpy_100c.lib_biblio100cols as lb100
import numpy as np
import pandas as pd
import io
import os
import datetime
from random import randrange
from datetime import timedelta


st.set_page_config(
    page_title="Club des 100 cols",
    page_icon="👋",
)

st.title('Bienvenue dans votre gestionaire de cols')

st.warning("Une fois les modifications réalisées n'oublié pas de télécharger vos données mise à jour.", icon="⚠️")

st.header('Charger les données')

st.session_state['filter_gpx']=False
st.session_state['id_f']=None
st.session_state['up_gpx']=None

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


st.header('Première connection')
st.subheader("Crée un profil")
st.markdown("Si c'est votre première utilisation et que vous n'avez pas encore un fichier *.100cols* compatible avec ce site commencé par crée un (ou plusieurs) nouvel utilisateur dans la section **Gestion des utilisateurs**.")

st.subheader('Démonstration')
st.markdown("Si vous voulez avoir un aperçu des possibles de l'application généré un profil aléatoire")

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
        
        
        
if st.button('Générer un utilisateur'):
        st.session_state['data_list'].append(lc.list100cols(id100col=1234,name='Michel Dupond',pseudo='Michel'))
        file=os.listdir('database/basecol/data_website/')
        colAll_list=[]
        for oo in file:
            colAll_list.append(lb100.list_biblio100cols(filename='database/basecol/data_website/'+oo).database)

        colsAll_tmp = pd.concat(colAll_list, axis=0, ignore_index=True)

        colAll=lb100.list_biblio100cols(filename='database/basecol/data_website/'+file[0])
        colAll.database=colsAll_tmp

        dinit=datetime.datetime(2000, 1, 1, 0, 0)
        dend=datetime.datetime.now()

        for i in range(768):
            id=np.random.randint(0,len(colAll.database))
            dd=random_date(dinit,dend).date()
            txt=st.session_state['data_list'][-1].add_pass(colAll.database.loc[id],dd)

        st.success('Un utilisateur a été crée !', icon="✅")



