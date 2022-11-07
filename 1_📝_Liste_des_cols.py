import streamlit as st
import time
import numpy as np
import pickle
import io
import datetime

st.set_page_config(page_title="Liste des cols", page_icon="📝")

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
    st.title("Liste des cols de "+ option)
    if len(st.session_state['data_list'][st.session_state['id_u']].cols)==0:
        st.warning(st.session_state['data_list'][st.session_state['id_u']].name+" n'a pas encore de col enregistré.")
    else:
        st.write(option+' a fait '+str(len(st.session_state['data_list'][st.session_state['id_u']].cols))+' cols, dont '+str(np.sum(st.session_state['data_list'][st.session_state['id_u']].cols.Altitude>2000))+' de plus de 2000 m.')
        fu_id=st.text_input('Code',label_visibility="visible",key='fcode')
        fu_nom=st.text_input('Nom',label_visibility="visible",key='fnom')
        malt=int(np.array(st.session_state['data_list'][st.session_state['id_u']].cols.Altitude).max())
        fu_alt=st.slider('Altitudes :', 0, malt, (0, malt))

        min_date=st.session_state['data_list'][st.session_state['id_u']].cols.Date.min()
        max_date=st.session_state['data_list'][st.session_state['id_u']].cols.Date.max()

        fu_date = st.date_input(
            "Date :",
            value=(min_date, max_date))


        if len(fu_date)==1:
            fu_date=(fu_date[0],max_date)


        id=st.session_state['data_list'][st.session_state['id_u']].filter_name(fu_nom,dep=fu_id,alt=fu_alt,date=fu_date,print_res=False)

        st.info(str(np.sum(id))+' cols correspondent aux filtres', icon="ℹ️")

        st.dataframe(st.session_state['data_list'][st.session_state['id_u']].cols.loc[id])
