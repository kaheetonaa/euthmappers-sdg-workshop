import streamlit as st
from pymongo import MongoClient
import pandas as pd
import altair as alt

st.set_page_config(
        page_title="🌐 EuthMappers quizz result",
        page_icon="✅",
        layout="wide"
)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@100&display=swap'); 

    html, body, h1,h2,h3,p{
        font-family: 'Comfortaa', sans-serif; 
        
    }
    div[data-baseweb="select"] > div {
    background-color: #62cbec10;
            color:white;
            font-family: 'Comfortaa', sans-serif;
    }

    body{
        font-size: 18px;
        gap: 20px;
    }

    [role=radiogroup]{
        gap: 1rem;
    }
    h1 {
        text-align: center
    }
    h2 {
        text-align: center
    }
    h3 {
        text-align: center
    }
    
    div[data-testid='stVerticalBlockBorderWrapper']{
        background-color: #ffffffC0;
    }
            .center {
    display: block;
    margin-left: auto;
    margin-right: auto;
        width:200px;
            }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = init_connection()

db=client['EuthMappers_SDG_241126']
collection=db['EuthMappers_SDG_241126']
st.title('Which SDG is .... ?')
container1 = st.container()
placeholder = st.empty()
domain = ["🇮🇹Italy", "🇵🇹Portugal", "🇷🇴Romania", "🇸🇰Slovakia", "🇪🇸Spain"]
range_ = ['#B9F3E3', '#F5716C', '#F5CC81', '#6799A3', '#F5996F']
click = alt.selection_point(encodings=['color'])

color = alt.condition(
    click,
    alt.Color('school:N').scale(domain=domain,range=range_),
    alt.value('lightgray')
)
result=pd.DataFrame(list(collection.find()))
result0=result.groupby(['1','school']).count().reset_index()
with container1:
    st.html("<img src='https://raw.githubusercontent.com/kaheetonaa/streamlit_quizz_template_euth/refs/heads/main/asset/logo.png' class='center'/>")
    st.markdown(""" ___""")
    result
    chart1A = alt.Chart(result0,title='question 01').mark_bar().encode(
            x='1',
            y='1',
            color=color
        ).add_params(
            click
        ).properties(height=300,width=300)
    for i in range(16):
        if(i<9):
            st.image('asset/sdg-icon/E-WEB-Goal-0'+str(i+1)+'.png',width=100)
        else:
            st.image('asset/sdg-icon/E-WEB-Goal-'+str(i+1)+'.png',width=100)
