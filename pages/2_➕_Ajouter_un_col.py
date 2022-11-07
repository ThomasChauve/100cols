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
import gpxpy

st.set_page_config(page_title="Ajouter un col", page_icon="➕")

if 'id_u' not in st.session_state:
    st.session_state['id_u'] = 0

if 'data_list' not in st.session_state:
    st.session_state['data_list']=[]

if 'filter_gpx' not in st.session_state:
    st.session_state['filter_gpx']=False

user_list=[]
for du in st.session_state['data_list']:
    user_list.append(du.pseudo)

def pickle_model(model):
    f = io.BytesIO()
    pickle.dump(model.__dict__, f)
    return f 

def load_gpx(gpxfile):
    gpx = gpxpy.parse(gpxfile)

    # Convert to a dataframe one point at a time.
    points = []
    for segment in gpx.tracks[0].segments:
        for p in segment.points:
            points.append({
                'time': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })
    df = pd.DataFrame.from_records(points)
    return df

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
    uploaded_gpx = st.file_uploader("Charger une trace",type='gpx',accept_multiple_files=False)
    
    if len(op_ly)!=0:
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
        if uploaded_gpx is not None:
            df_gpx=load_gpx(uploaded_gpx)
        else:
            df_gpx=None
        
        if (df_gpx is not None):
            if st.button('Filtrer avec la trace gpx') or st.session_state['filter_gpx']:
                filter_gpx=True
                st.session_state['filter_gpx']=True
                id_nb=np.where(id==True)
                lim=10**-4
                gg=np.array(df_gpx)[:,1:3]
                my_bar = st.progress(0)
                k=0
                for i in id_nb[0]:
                    v=(gg[:,::-1]-np.array(colAll.database.loc[i][4:6]))
                    nn=np.linalg.norm(np.float32(v),axis=1).min()
                    if nn > lim:
                        id[i]=False
                    k+=1
                    my_bar.progress(k/len(id_nb[0]))


        st.dataframe(colAll.database.loc[id])

        if np.sum(id)<5000:
            with st.expander("Montrer sur la carte :"):
                fig_map=colAll.plot_map(id,ww=width,gpx=df_gpx)
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
        if st.session_state['filter_gpx']:
            if st.button('Ajouter tous les cols'):
                for i in list(np.where(id)[0]):
                    txt=st.session_state['data_list'][st.session_state['id_u']].add_pass(colAll.database.loc[i],f_date)
                    if 'ajouter' in txt:
                        st.success(txt, icon="✅")
                    else:
                        st.warning(txt, icon="⚠️")
