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
    
    div[data-testid='stAppViewBlockContainer']{
        background-color: #62cbec10;
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
for i in range(16):
    if(i<9):
        st.image('asset/sdg-icon/E-WEB-Goal-0'+str(i+1)+'.png',width=100)
    else:
        st.image('asset/sdg-icon/E-WEB-Goal-'+str(i+1)+'.png',width=100)
