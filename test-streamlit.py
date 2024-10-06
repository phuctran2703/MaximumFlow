import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Setup full screen
st.set_page_config(layout="wide")

# Start and end point
st.sidebar.title("Tìm kiếm")

start_point = st.sidebar.text_input("Điểm đi:", placeholder="Nhập địa chỉ hoặc tọa độ")

end_point = st.sidebar.text_input("Điểm đến:", placeholder="Nhập địa chỉ hoặc tọa độ")

# Choose an algorithm
algorithm = st.sidebar.selectbox(
    "Chọn thuật toán:",
    ("Thuật toán 1", "Thuật toán 2", "Thuật toán 3")
)

# Create map
map_center = [10.7769, 106.6670]  # district 10, ho chi minh
mymap = folium.Map(location=map_center, zoom_start=15)

# Create geolocator to find location
geolocator = Nominatim(user_agent="CO_SO_TOAN")

# find location
start_locations = geolocator.geocode(start_point, exactly_one=False, limit=3)
end_locations = geolocator.geocode(end_point, exactly_one=False, limit=3)

# Show find results in sidebar
if start_locations:
    for location in start_locations:    
        # Show find results

        if st.sidebar.button(location.address):
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=location.address
            ).add_to(mymap)
            mymap.location = [location.latitude, location.longitude]
            mymap.zoom_start = 18

if end_locations:
    for location in end_locations:    
        # Show find results
        if st.sidebar.button(location.address):
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=location.address
            ).add_to(mymap)
            mymap.location = [location.latitude, location.longitude]
            mymap.zoom_start = 18

# Show map
st_folium(mymap, width=1400, height=700)