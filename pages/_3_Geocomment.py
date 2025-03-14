import streamlit as st
import requests
import geopandas as gpd
import folium
from folium.features import GeoJsonPopup
from streamlit_folium import st_folium
from pymongo import MongoClient


st.set_page_config(
  page_title="🌐 EuthMappers quizz",
  page_icon="❓",
  layout="wide"
)

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = init_connection()

db=client['EuthMappers_Geocomment_241126']
collection=db['EuthMappers_Geocomment_241126']


st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@100&display=swap'); 

    html, body, h1,h2,h3,p{
        font-family: 'Comfortaa', sans-serif; 
        
    }
    div[data-baseweb="select"] > div {
    background-color: #62cbec10;
            color:black;
            font-family: 'Comfortaa', sans-serif;
    }

    body{
        font-size: 18px;
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
st.html("<img src='https://raw.githubusercontent.com/kaheetonaa/streamlit_quizz_template_euth/refs/heads/main/asset/logo.png' class='center'/>")
st.markdown(""" ___""")
popup = GeoJsonPopup(
    fields=['projecId-str']
)
def load_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        raise
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        raise

def style_function(feature):
    props = feature.get('properties')
    markup = f"""
            <div style="width: 20px;
                        height: 20px;
                        border: 1px solid red;
                        border-radius: 10px;
                        background-color: #ff000030;">
            </div>
        </div>
    """
    return {"html": markup}
st.title('Where humanitarian mapping with Sustainable Development Goals taken in consideration can be applied?')
@st.fragment
def drawMap(popup,location,zoom):
    map = folium.Map(
    location=location, zoom_start=zoom, max_zoom=21)
    if options!=0:
        org_json = folium.GeoJson(data=gdf,
                                marker=folium.Marker(icon=folium.DivIcon()),
                                style_function=style_function,
        popup=popup)
        org_json.add_to(map)
    st_map= st_folium(
    map,
    width='100%',
    height=500
    )
    st.session_state.location=[st_map['center']['lat'],st_map['center']['lng']]
    st.session_state.zoom=st_map['zoom']
    st.session_state.bounds=st_map['bounds']
    st.session_state.last_object_clicked_popup=st_map['last_object_clicked_popup']
    if st.session_state.last_object_clicked_popup !=None:
        print(st.session_state.last_object_clicked_popup)
        link="https://tasks.hotosm.org/projects/"+st.session_state.last_object_clicked_popup
        st.link_button("Go to project", str(link).replace('\n', '').replace(' ','').replace('projecId-str',''))
    else:
        st.write('No project has been selected')

org_str=["None","UN+Mappers", "Missing%20Maps", "M%C3%A9decins%20Sans%20Fronti%C3%A8res%20%28MSF%29%20","USAID","HOT"]
org_name=["None","UN Mappers", "Missing Maps", "Médecins Sans Frontières","USAID","HOT"]
org_index = list(range(len(org_name)))

#select natioin
def submit_answer():
    if (comment!="")&(school!=None):
            post={'school':school,'bounds':'POLYGON (('+str(st.session_state.bounds['_southWest']['lng'])+' '+str(st.session_state.bounds['_southWest']['lat'])+','+str(st.session_state.bounds['_southWest']['lng'])+' '+str(st.session_state.bounds['_northEast']['lat'])+','+str(st.session_state.bounds['_northEast']['lng'])+' '+str(st.session_state.bounds['_northEast']['lat'])+','+str(st.session_state.bounds['_northEast']['lng'])+' '+str(st.session_state.bounds['_southWest']['lat'])+','+str(st.session_state.bounds['_southWest']['lng'])+' '+str(st.session_state.bounds['_southWest']['lat'])+'))','comment':comment,'center':'POINT ('+str(st.session_state.location[1])+' '+str(st.session_state.location[0])+')','zoom':st.session_state.zoom}
            collection.insert_one(post)
            st.session_state.answer_submitted=True;
    else:
        st.warning('you have to select your school and write your comment!')

if "answer_submitted" not in st.session_state:
    school = st.selectbox(
        "Where is your school",
        ("🇮🇹Italy", "🇵🇹Portugal", "🇷🇴Romania", "🇸🇰Slovakia", "🇪🇸Spain"),index=None
        )
    #form
    comment = st.text_input("Zoom to an area where you think suitable for the project then write down your comment. Finally hit Enter to submit", "")
    st.button('Submit', on_click=submit_answer)      

    #referencing
    options = st.selectbox(
        "Choose the organization to see their active/archived projects",options=org_index,format_func=lambda x: org_name[x]
    )

    url = "https://tasking-manager-tm4-production-api.hotosm.org/api/v2/projects/?orderBy=id&orderByType=ASC&mappingTypesExact=false&page=1&createdByMe=false&mappedByMe=false&favoritedByMe=false&managedByMe=false&basedOnMyInterests=false&omitMapResults=false&downloadAsCSV=false&organisationName="+org_str[options]
    archived=st.checkbox('Archived projects')
    if archived:
        url=url+"&projectStatuses=ARCHIVED"

    if options!=0:
        data = load_json_from_url(url)
        geom_data=data['mapResults']['features']
        gdf = gpd.GeoDataFrame.from_features(geom_data).set_crs(epsg=4326)
        gdf['x']=gdf.geometry.x
        gdf['y']=gdf.geometry.y
        gdf['dummy']=1
        gdf['projecId-str']=gdf['projectId'].map(str)

    if 'location' not in st.session_state:
        st.session_state.location = [0, 0]
    if 'zoom' not in st.session_state:
        st.session_state.zoom = 5
    #map
    a=drawMap(popup,st.session_state.location,st.session_state.zoom)
else:
    st.balloons();
    st.write('You have sucessfully submitted!')








