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
def submit_answer():
    if (comment!="")&(school!=None):
            st.write(school, comment)
            post={'school':school,'comment':comment}
            collection.insert_one(post)
            st.session_state.answer_submitted=True
            st.write(st.session_state.answer_submitted)
    else:
            st.warning('you have to select your school and write your comment!')

if "answer_submitted" not in st.session_state:
    school = st.selectbox(
        "Where is your school",
        ("🇮🇹Italy", "🇵🇹Portugal", "🇷🇴Romania", "🇸🇰Slovakia", "🇪🇸Spain"),index=None
        )

        #form
        st.image('asset/sdg-icon/E-WEB-Goal-01.png')
    comment = st.multiselect(
    "What are your favorite colors",
    ['Goal 1. No poverty',
'Goal 2. Zero hunger',
'Goal 3. Good health and well-being',
'Goal 4. Quality education',
'Goal 5. Gender equality',
'Goal 6. Clean water and sanitation',
'Goal 7. Affordable and clean energy',
'Goal 8. Decent work and economic growth',
'Goal 9. Industry, innovation and infrastructure',
'Goal 10. Reduced inequalities',
'Goal 11. Sustainable cities and communities',
'Goal 12. Responsible consumption and production',
'Goal 13. Climate action',
'Goal 14. Life below water',
'Goal 15. Life on land',
'Goal 16. Peace, Justice and strong institution',
'Goal 17. Partnerships for the goals'],
    [],
)
    st.button('Submit', on_click=submit_answer)
else:
    st.balloons()
    st.write('You have successfully submit your answer!')

    




