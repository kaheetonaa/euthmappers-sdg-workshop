import geopandas as gpd
import osmium
from streamlit_folium import st_folium
import folium
from folium.features import GeoJsonPopup
import streamlit as st



st.set_page_config(layout="wide")
st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@100&display=swap'); 

    html, body, h1,h2,h3,p{
        font-family: 'Comfortaa', sans-serif; 
        
    }
    div[data-baseweb="select"] > div {
    background-color: #62cbec;
            color:white;
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

osm_data= osmium.FileProcessor("https://api06.dev.openstreetmap.org/api/0.6/map?bbox=105.85475%2C20.98985%2C105.86246%2C21.00602&include_discussion=true").with_areas().with_filter(osmium.filter.GeoInterfaceFilter())

START_LOCATION = [20.99174, 105.85906]
START_ZOOM = 18

features = gpd.GeoDataFrame.from_features(osm_data).set_crs(epsg=4326)

building=features[features.geometry.type=='MultiPolygon'][features.building.notnull()]
highway=features[features.geometry.type=='LineString'][features.highway.notnull()]

building_style = {"fillColor": "red", "fillOpacity": 0.2,"color":"red"}
highway_style = {"color":"white","weight":5}

building_popup = GeoJsonPopup(
    fields=list(building.columns)[1:],

)

highway_popup = GeoJsonPopup(
    fields=list(highway.columns)[1:],

)

building_json = folium.GeoJson(data=building, style_function=lambda _x: building_style,popup=building_popup)
highway_json = folium.GeoJson(data=highway, style_function=lambda _x: highway_style,popup=highway_popup)

map = folium.Map(
    location=START_LOCATION, zoom_start=START_ZOOM, max_zoom=21
)

folium.TileLayer(name='ESRI',tiles='https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}?blankTile=false',attr='esri',max_zoom=21,max_native_zoom=18,opacity=1).add_to(map)




fg = folium.FeatureGroup(name="Parcels",control=True)
fg = fg.add_child(building_json)
fg = fg.add_child(highway_json)

st_folium(
            map,
            width="100%",
            height=600,
            feature_group_to_add=fg,
            returned_objects=[]
)


#If btn is pressed or True
if st.button('Refresh'):
    #This would empty everything inside the container
    st.empty()

