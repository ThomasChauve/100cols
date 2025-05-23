import streamlit as st
import pandas as pd
import numpy as np
import libpy_100c.libpy_100c as lc
import libpy_100c.lib_biblio100cols as lb100
import pickle
import io
import os
import datetime
import gpxpy
import gc

st.set_page_config(page_title="Ajouter un col", page_icon="➕")

if 'id_u' not in st.session_state:
    st.session_state['id_u'] = 0

if 'data_list' not in st.session_state:
    st.session_state['data_list']=[]

if 'filter_gpx' not in st.session_state:
    st.session_state['filter_gpx']=False

if 'id_f' not in st.session_state:
    st.session_state['id_f']=None

if 'up_gpx' not in st.session_state:
    st.session_state['up_gpx']=None

if 'd_date' not in st.session_state:
    st.session_state['d_date']=datetime.date.today()

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
    
    if st.button('Clean gpx'):
            st.session_state['filter_gpx']=False
            st.session_state['id_f']=None
            st.session_state['up_gpx']=None
            st.session_state['d_date']=datetime.date.today()
            uploaded_gpx=None
            st.success('Recherche gpx nettoyée', icon="✅")
            
    
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

        if st.session_state['filter_gpx']:
            id=st.session_state['id_f']
        else:
            id=colAll.filter_name(f_nom,dep=f_id,alt=aa,print_res=False)
        
        if uploaded_gpx is not None:
            df_gpx=load_gpx(uploaded_gpx)
        else:
            df_gpx=None

        if (df_gpx is not None):
            if st.button('Filtrer avec la trace gpx'):
                filter_gpx=True
                st.session_state['filter_gpx']=True
                id_nb=np.where(id==True)
                lim=2*10**-4
                gg=np.array(df_gpx)[:,1:3]
                gg=gg[:,::-1]
                with st.spinner('Recherche col sur la trace ...'):
                    if np.sum(id)<1000:
                        for i in id_nb[0]:
                            v=(gg-np.array(colAll.database.loc[i][4:6]))
                            nn=np.linalg.norm(np.float32(v),axis=1).min()
                            if nn > lim:
                                id[i]=False
                    else:
                        test=True
                        it=0
                        while test:
                            gcol=np.array(colAll.database)[it:it+1000,4:6]
                            xt,xc=np.meshgrid(gg[:,0],gcol[:,0])
                            res=(xt-xc)**2
                            xt,xc=np.meshgrid(gg[:,1],gcol[:,1])
                            res=(res+(xt-xc)**2)**0.5
                            res=np.min(res,axis=-1)
                            if it==0:
                                id=res<lim
                            else:
                                id=np.concatenate([id,res<lim])
                            it+=1000
                            if it>len(np.array(colAll.database)):
                                test=False
                st.session_state['d_date']=df_gpx.time.loc[0].to_pydatetime().date()                     
                st.success(str(np.sum(id))+' cols trouvés !')
                st.session_state['id_f']=id




        st.dataframe(colAll.database.loc[id])

        if np.sum(id)<5000:
            with st.expander("Montrer sur la carte :"):
                fig_map=colAll.plot_map(id,ww=width,gpx=df_gpx)
                st.plotly_chart(fig_map, use_container_width=True)
                

        st.header('Ajouter')

        f_date=st.date_input('Date de monté',value=st.session_state['d_date'], label_visibility="visible")

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
