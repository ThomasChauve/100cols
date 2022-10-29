import streamlit as st
import pandas as pd
import time
import numpy as np
import libpy_100c.libpy_100c as lc
import libpy_100c.lib_biblio100cols as lb100
import pickle
import io
import os
import datetime

st.set_page_config(page_title="Ajouter un col", page_icon="➕")

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
    st.title('Ajouter un col')
    st.warning("Pas d'utilisateur enregistré")
else:
    st.title('Ajouter un col à '+option)
    file=os.listdir('database/basecol/data_website/')
    op_ly = st.multiselect('Librairie :',file,default='France.csv')
    colAll_list=[]
    for oo in op_ly:
        colAll_list.append(lb100.list_biblio100cols(filename='database/basecol/data_website/'+oo).database)
    
    colsAll_tmp = pd.concat(colAll_list, axis=0, ignore_index=True)
    
    colAll=lb100.list_biblio100cols(filename='database/basecol/data_website/'+op_ly[0])
    colAll.database=colsAll_tmp
                  
    st.header('Recherche')

    f_id=st.text_input('Code',label_visibility="visible")
    f_nom=st.text_input('Nom',label_visibility="visible")
    f_alt=st.number_input('Altitude', label_visibility="visible",min_value=int(0))


    if f_alt==0:
        aa=None
    else:
        aa=f_alt


    id=colAll.filter_name(f_nom,dep=f_id,alt=aa,print_res=False)
    st.dataframe(colAll.database.loc[id])
    
    if np.sum(id)<5000:
        with st.expander("Montrer sur la carte :"):
            fig_map=colAll.plot_map(id,ww=width)
            st.plotly_chart(fig_map, use_container_width=True, sharing="streamlit")

    st.header('Ajouter')

    f_date=st.date_input('Date de monté', label_visibility="visible")

    add_code = st.selectbox('Col à ajouter',colAll.database.loc[id])

    
    if st.button('Ajouter'):
        index=list(colAll.database[colAll.database.columns[0]]).index(add_code)
        
        txt=st.session_state['data_list'][st.session_state['id_u']].add_pass(colAll.database.loc[index],f_date)
        if 'ajouter' in txt:
            st.success(txt, icon="✅")
        else:
            st.warning(txt, icon="⚠️")
