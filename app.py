import streamlit as st
from PIL import Image
import tempfile
from inference import predict_warning_light
import json
from datetime import datetime
import base64
from streamlit_folium import st_folium
from geopy.distance import geodesic
import folium

st.set_page_config(page_title="Vehicle Maintenance Predictor", layout="wide")

# --- Save to History ---
def append_to_history(prediction, image_bytes):
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    image_base64 = base64.b64encode(image_bytes).decode()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "labels": [prediction["label"]],
        "recommendations": prediction.get("recommendation", []),
        "image": f"data:image/jpeg;base64,{image_base64}"
    }

    history.insert(0, entry)

    with open("history.json", "w") as f:
        json.dump(history, f, indent=2)

# --- Load Service Centers ---
def load_service_centers():
    with open("service_centers.json", "r") as f:
        return json.load(f)

# --- Navigation Bar ---
st.markdown("""
<style>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 40px;
    background-color: #f9fafb;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-bottom: 1px solid #e5e7eb;
    font-family: 'Segoe UI', sans-serif;
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 15px;
}
.nav-left img {
    height: 24px;
}
.nav-links a {
    margin: 0 12px;
    text-decoration: none;
    color: #6b7280;
    font-weight: 500;
}
.nav-links a:hover, .nav-links a.active {
    color: #2563eb;
}
.nav-right {
    display: flex;
    gap: 10px;
    align-items: center;
}
.nav-right button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 14px;
    cursor: pointer;
    font-weight: 500;
}
</style>
<div class='navbar'>
  <div class='nav-left'>
    <img src='https://img.icons8.com/ios-filled/50/2563eb/car--v1.png'/>
    <div class='nav-left'>
      <div style='display: flex; align-items: center; gap: 8px;'>
        <span style='font-size: 1.4em; font-weight: 600; color: #111827;'>AutoVision</span>
        <span style='background-color:#2563eb; color:white; font-size: 0.65em; padding: 2px 6px; border-radius: 6px;'>BETA</span>
      </div>
    </div>
  </div>
  <div class='nav-links'>
    <a href="/" class="active">🏠 Home</a>
    <a href="/History" target="_self">🕒 History</a>
    <a href="#service">📍 Service Centers</a>
    <a href="#profile">👤 Profile</a>
  </div>
  <div class='nav-right'>
    <span style='color: #111827;'>Sign in</span>
    <button onclick="window.location.href='#upload'">Analyze Dashboard</button>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div style='text-align: center; padding-top: 30px;'>
    <h1 style='font-size: 3em; color: #2563eb;'>Predict Vehicle Maintenance Before Issues Arise</h1>
    <p style='font-size: 1.2em;'>Upload your dashboard image and get early maintenance predictions using our advanced AI technology</p>
    <a href="#upload"><button style='padding: 10px 20px; background-color: #2563eb; color: white; border-radius: 8px;'>Get Started →</button></a>
    <a href="/History" target="_self">
      <button style='padding: 10px 20px; background-color: white; color: #2563eb; border: 1px solid #2563eb; border-radius: 8px;'>View History</button>
    </a>
</div>
""", unsafe_allow_html=True)

# --- How It Works Section ---
st.markdown("<h2 style='padding-top: 60px;'></h2>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div style='padding: 20px;'>
        <h3 style='margin-bottom: 30px; font-size: 1.7em;'>How It Works</h3>
        <div style='margin-bottom: 30px;'>
            <div style='display: flex; align-items: flex-start;'>
                <div style='font-size: 1.1em; background-color: #dbeafe; color: #1e40af; border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; font-weight: bold;'>1</div>
                <div style='margin-left: 15px;'>
                    <div style='font-weight: 600; font-size: 1.2em;'>Upload Your Dashboard Image</div>
                    <div style='font-size: 1.05em; color: #ccc;'>Take a clear photo showing warning lights</div>
                </div>
            </div>
        </div>
        <div style='margin-bottom: 30px;'>
            <div style='display: flex; align-items: flex-start;'>
                <div style='font-size: 1.1em; background-color: #dbeafe; color: #1e40af; border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; font-weight: bold;'>2</div>
                <div style='margin-left: 15px;'>
                    <div style='font-weight: 600; font-size: 1.2em;'>AI Analysis</div>
                    <div style='font-size: 1.05em; color: #ccc;'>We identify the warning lights for you</div>
                </div>
            </div>
        </div>
        <div>
            <div style='display: flex; align-items: flex-start;'>
                <div style='font-size: 1.1em; background-color: #dbeafe; color: #1e40af; border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; font-weight: bold;'>3</div>
                <div style='margin-left: 15px;'>
                    <div style='font-weight: 600; font-size: 1.2em;'>Get Maintenance Recommendations</div>
                    <div style='font-size: 1.05em; color: #ccc;'>Receive detailed advice to fix the issue</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 id='upload'>Upload Dashboard Image</h3>", unsafe_allow_html=True)
    upload_method = st.radio("Select input method", ["Upload Image", "Open Camera"], horizontal=True)

    img_bytes = None
    if upload_method == "Upload Image":
        uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_bytes = uploaded_file.read()
    elif upload_method == "Open Camera":
        camera_image = st.camera_input("📸 Take a picture")
        if camera_image:
            img_bytes = camera_image.getvalue()

if img_bytes:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(img_bytes)
        img_path = tmp_file.name

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(Image.open(img_path), caption="Uploaded Image", use_container_width=True)

    with col2:
        with st.spinner("Analyzing dashboard image..."):
            result = predict_warning_light(img_path)

        append_to_history(result, img_bytes)

        st.markdown(f"""
        <div style='border: 1px solid #333; padding: 20px; border-radius: 10px; background-color: #1e1e1e; color: #f1f1f1; margin-top: 20px;'>
            <h3 style='color: #60a5fa;'>🔍 Analysis Results</h3>
            <p><strong>🔧 Label:</strong> <span style='background-color:#166534; color:#dcfce7; padding: 4px 10px; border-radius: 4px;'>{result['label']}</span></p>
            <p><strong>📊 Confidence:</strong> <span style='color:#facc15;'>{result['confidence']}%</span></p>
            <p><strong>📄 Description:</strong> {result['description']}</p>
            <p><strong>🚨 Severity:</strong> <span style='background-color:#7f1d1d; color:#fee2e2; padding: 4px 10px; border-radius: 4px;'>{result['severity']}</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top: 30px;'>
            <h3 style='color:#facc15;'>🛠 Maintenance Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)

        for rec in result.get("recommendation", []):
            st.markdown(f"""
            <div style='padding: 15px; background-color: #2c2c2c; border-left: 4px solid #f87171; border-radius: 6px; color: #f1f1f1; margin-bottom: 10px;'>
                {rec}
            </div>
            """, unsafe_allow_html=True)

        centers = load_service_centers()
        matched = [c for c in centers if result["label"] in c["specialties"]]

        # --- Map + Distance Section ---
        user_lat = st.number_input("📍 Enter your latitude", value=6.9271, step=0.01)
        user_lon = st.number_input("📍 Enter your longitude", value=79.8612, step=0.01)
        user_location = (user_lat, user_lon)

        st.markdown("<h3 style='margin-top: 30px; color:#2563eb;'>📍 Service Center Locations</h3>", unsafe_allow_html=True)
        map_col, list_col = st.columns([1.2, 1.3])


        with map_col:
            service_map = folium.Map(location=user_location, zoom_start=10)
            folium.Marker(user_location, tooltip="You are here", icon=folium.Icon(color="blue")).add_to(service_map)

            for center in matched:
                coord = (center["latitude"], center["longitude"])
                dist_km = round(geodesic(user_location, coord).km, 2)
                popup_text = f"{center['name']}<br>{center['address']}<br>Distance: {dist_km} km"
                folium.Marker(coord, tooltip=center["name"], popup=popup_text, icon=folium.Icon(color="green")).add_to(service_map)

            st_folium(service_map, height=500)


        with list_col:
            for center in matched[:5]:
                coord = (center["latitude"], center["longitude"])
                distance = round(geodesic(user_location, coord).km, 2)
                st.markdown(f"""
                <div style='background-color:#f9fafb; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #2563eb; color: #111827;'>
                    <b>{center['name']}</b><br>
                    📍 {center['address']}<br>
                    📞 {center.get('contact', 'N/A')}<br>
                    🧭 Distance: <b>{distance} km</b><br>
                    🔧 Specialties: <i>{', '.join(center['specialties'])}</i>
                </div>
                """, unsafe_allow_html=True)
