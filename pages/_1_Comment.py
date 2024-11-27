import streamlit as st
from pymongo import MongoClient
st.set_page_config(layout="wide")
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

db=client['EuthMappers_Forum_241126']
collection=db['EuthMappers_Forum_241126']
st.title('What is Sustainable Development ?')
container1 = st.container()
def submit_answer():
        if (comment!="")&(school!=None):
                st.write(school, comment)
                post={'school':school,'comment':comment}
                collection.insert_one(post)
                st.session_state.answer_submitted=True
                st.write(st.session_state.answer_submitted)
        else:
                st.warning('you have to select your school and write your comment!')
with container1:
    st.html("<img src='https://raw.githubusercontent.com/kaheetonaa/streamlit_quizz_template_euth/refs/heads/main/asset/logo.png' class='center'/>")
    st.markdown(""" ___""")

    if "answer_submitted" not in st.session_state:
        school = st.selectbox(
            "Where is your school",
            ("🇮🇹Italy", "🇵🇹Portugal", "🇷🇴Romania", "🇸🇰Slovakia", "🇪🇸Spain"),index=None
            )

            #form
        comment = st.text_input("What is Sustainable Development?", "")
        st.button('Submit', on_click=submit_answer)
    else:
        st.balloons()
        st.write('You have successfully submit your answer!')

        




