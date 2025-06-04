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

st.set_page_config(
    page_title="AutoVision - Vehicle Maintenance Predictor", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS Styling
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    body {
    margin-top: 0 !important;
}

html {
    scroll-behavior: smooth;
}

    
    .main .block-container {
    padding-top: 110px !important;
    padding-bottom: 2rem;
    background: transparent;
}


    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
            
    
    
    /* Modern Navigation Bar */
    .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 48px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(229, 231, 235, 0.3);
    box-shadow: 0 1px 20px rgba(0, 0, 0, 0.05);
    margin-bottom: 0;
}

    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
    }
    
    .nav-brand img {
        height: 32px;
        width: 32px;
    }
    
    .brand-text {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .beta-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
        margin-left: 8px;
    }
    
    .nav-links {
        display: flex;
        gap: 32px;
        align-items: center;
    }
    
    .nav-links a {
        text-decoration: none;
        color: #6b7280;
        font-weight: 500;
        font-size: 15px;
        transition: all 0.2s ease;
        padding: 8px 16px;
        border-radius: 8px;
    }
    
    .nav-links a:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    .nav-links a.active {
        color: #667eea;
        background: rgba(102, 126, 234, 0.15);
    }
    
    .nav-actions {
        display: flex;
        gap: 16px;
        align-items: center;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4), 0 0 20px #667eea66;
}

    
    .btn-secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }

    .btn-primary, .btn-secondary {
    transition: all 0.25s ease;
    transform: translateY(0px);
}

.btn-primary:hover, .btn-secondary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}
     
    
    /* Hero Section */
    .hero-section {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 60px 20px 70px 20px;  /* top, right, bottom, left */
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    margin: 0 -1rem;
    border-radius: 40px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
}
    .hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 30%, #667eea40, transparent 50%),
                radial-gradient(circle at 70% 60%, #764ba240, transparent 50%),
                radial-gradient(circle at 50% 90%, #8b5cf640, transparent 60%);
    animation: auroraMove 25s linear infinite;
    z-index: 0;
    opacity: 0.8;
}

@keyframes gridScroll {
    0% {
        background-position: 0 0, 0 0;
    }
    100% {
        background-position: 100px 100px, 100px 100px;
    }
}


.hero-section > * {
    position: relative;
    z-index: 1;
}


    
    .hero-title {
        font-size: 7.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 24px;
        line-height: 1.2;
    }
    
    .hero-title {
    font-size: 7.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 24px;
    line-height: 1.2;
    animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
    
    .hero-subtitle {
    font-size: 1.25rem;
    color: #6b7280;
    margin-bottom: 40px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
    text-align: center;
}

            .btn-secondary:hover {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}
    
    .hero-buttons {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    /* How It Works Section */
    .how-it-works {
        padding: 80px 0;
        background: transparent;
    }
    
    .section-title {
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 60px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

    
    .steps-container {
        display: flex;
        flex-direction: column;
        gap: 40px;
        max-width: 600px;
    }
    
    .step {
        display: flex;
        align-items: flex-start;
        gap: 20px;
        padding: 30px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .step:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    }
    
    .step-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 20px;
        flex-shrink: 0;
    }
    
    .step-content h4 {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 8px;
    }
    
    .step-content p {
        color: #6b7280;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Upload Section */
    .upload-section {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-top: 40px;
    }
    
    .upload-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 30px;
    text-align: center;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
            .upload-section {
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.07);
    margin-top: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
}


    
    /* Analysis Results */
    .analysis-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .analysis-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .result-item {
        margin-bottom: 15px;
        font-size: 1rem;
    }
    
    .result-label {
        font-weight: 600;
        margin-right: 10px;
    }
    
    .label-badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .confidence-badge {
        color: #fbbf24;
        font-weight: 700;
    }
    
    .severity-badge {
        background: rgba(239, 68, 68, 0.3);
        color: #fecaca;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Recommendations */
    .recommendations-section {
        margin-top: 40px;
    }
    
    .recommendations-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .recommendation-item {
        background: white;
        padding: 20px;
        border-left: 4px solid #667eea;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        color: #374151;
        line-height: 1.6;
    }
    
    /* Service Centers */
    .service-centers-section {
        margin-top: 60px;
    }
    
    .service-centers-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .service-center-card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
        border-left: 4px solid #667eea;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .service-center-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    .service-center-name {
        font-weight: 700;
        font-size: 1.2rem;
        color: #1f2937;
        margin-bottom: 10px;
    }
    
    .service-center-info {
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 5px;
    }
    
    .distance-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Location inputs */
    .location-inputs {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        margin: 30px 0;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
            
    .btn-primary:hover .arrow {
    transform: translateX(4px);
}

.btn-primary {
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
}
            
            
    
    /* Responsive design */
    @media (max-width: 768px) {
        .navbar {
            padding: 16px 24px;
            flex-direction: column;
            gap: 20px;
        }
        
        .nav-links {
            gap: 20px;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-buttons {
            flex-direction: column;
            align-items: center;
        }
        
        .step {
            padding: 20px;
        }
        
        .upload-section {
            padding: 25px;
        }
    }
            
            .how-it-works-container {
    display: flex;
    gap: 40px;
    align-items: flex-start;
    justify-content: center;
    margin-top: 40px;
}

.steps-side, .upload-side {
    flex: 1;
    max-width: 600px;
}

@media (max-width: 768px) {
    .how-it-works-container {
        flex-direction: column;
        align-items: center;
    }
}

            
            .footer-fixed {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    text-align: center;
    padding: 16px 0;
    font-size: 0.95rem;
    color: #6b7280;
    box-shadow: 0 -1px 10px rgba(0, 0, 0, 0.05);
    border-top: 1px solid rgba(229, 231, 235, 0.5);
    z-index: 1000;
    backdrop-filter: blur(10px);
}
            .footer-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    text-align: center;
    padding: 12px 0;
    font-size: 0.95rem;
    font-weight: 500;
    color: #4b5563;
    border-top: 1px solid rgba(226, 232, 240, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    z-index: 999;
}

.footer-logo {
    height: 20px;
    width: 20px;
    margin-bottom: 2px;
}


</style>
""", unsafe_allow_html=True)

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

# --- Enhanced Navigation Bar ---
st.markdown("""
<div class='navbar'>
    <div class='nav-brand'>
        <img src='https://img.icons8.com/fluency/48/car--v1.png' alt='AutoVision Logo'/>
        <div>
            <span class='brand-text'>AutoVision</span>
            <span class='beta-badge'>BETA</span>
        </div>
    </div>
    <div class='nav-links'>
        <a href="/" class="active">🏠 Home</a>
        <a href="/History" target="_self">📊 History</a>
        <a href="#service">📍 Service Centers</a>
        <a href="#profile">👤 Profile</a>
    </div>
    <div class='nav-actions'>
        <span style='color: #6b7280; font-weight: 500;'>Welcome back!</span>
        <button class='btn-primary' onclick="document.getElementById('upload-section').scrollIntoView({behavior: 'smooth'})">
            Start Analysis →
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Enhanced Hero Section ---
st.markdown("""
<div class='hero-section'>
    <h1 class='hero-title'>
        Drive With Confidence.<br>Maintain Before It Breaks.
    </h1>
    <div class='hero-buttons'>
        <button class='btn-primary' onclick="document.getElementById('upload-section').scrollIntoView({behavior: 'smooth'})">
    <span style="margin-right: 8px;">🚀</span>
    Get Started Now
    <span style="margin-left: 8px; transition: transform 0.3s ease;" class="arrow">→</span>
</button>
        <a href="/History" target="_self">
            <button class='btn-secondary'>📈 View Analysis History</button>
        </a>
        <a href="#how-it-works">
            <button class='btn-secondary'>📘 Learn How It Works</button>
        </a>
    </div>
    <div style="margin-top: 30px; display: inline-flex; align-items: center; background: linear-gradient(135deg, #e0fce0, #d1fae5); color: #065f46; padding: 12px 20px; border-radius: 16px; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.3);">
    <span style="margin-right: 8px;">✅</span> Trusted by 500+ vehicle owners across Sri Lanka
</div>

</div>
""", unsafe_allow_html=True)


# --- How It Works Section ---
st.markdown("""
<div class='how-it-works' id='how-it-works'>
  <div class='how-it-works-container'>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("""
    <div class='steps-side'>
      <h2 class='section-title'>How It Works</h2>
      <div class='steps-container'>
          <div class='step'>
              <div class='step-number'>1</div>
              <div class='step-content'>
                  <h4>📱 Upload Dashboard Image</h4>
                  <p>Take a clear photo of your vehicle's dashboard showing any warning lights or indicators that concern you.</p>
              </div>
          </div>
          <div class='step'>
              <div class='step-number'>2</div>
              <div class='step-content'>
                  <h4>🤖 AI-Powered Analysis</h4>
                  <p>Our advanced computer vision system analyzes your image to identify warning lights and potential issues.</p>
              </div>
          </div>
          <div class='step'>
              <div class='step-number'>3</div>
              <div class='step-content'>
                  <h4>🔧 Get Expert Recommendations</h4>
                  <p>Receive detailed maintenance advice and find nearby service centers specialized in your vehicle's needs.</p>
              </div>
          </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# --- Upload Section ---
with col2:
    st.markdown("""
    <div class='upload-side'>
      <h2 class='section-title'>🎯 Upload Dashboard Image</h2>
      <div class='upload-section' id='upload-section'>
    """, unsafe_allow_html=True)

    upload_method = st.radio(
        "Select input method", 
        ["📤 Upload Image", "📸 Open Camera"], 
        horizontal=True,
        key="upload_method"
    )

    img_bytes = None
    if upload_method == "📤 Upload Image":
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of your vehicle's dashboard"
        )
        if uploaded_file:
            img_bytes = uploaded_file.read()
    elif upload_method == "📸 Open Camera":
        camera_image = st.camera_input("Take a picture of your dashboard")
        if camera_image:
            img_bytes = camera_image.getvalue()

    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("""
  </div> <!-- end of how-it-works-container -->
</div> <!-- end of how-it-works -->
""", unsafe_allow_html=True)
# --- Upload Section ---

# --- Analysis Results ---
if img_bytes:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(img_bytes)
        img_path = tmp_file.name

    st.markdown("<div style='margin-top: 60px;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.image(
            Image.open(img_path), 
            caption="📷 Uploaded Dashboard Image", 
            use_container_width=True
        )

    with col2:
        with st.spinner("🔍 Analyzing dashboard image..."):
            result = predict_warning_light(img_path)

        # Save to history
        append_to_history(result, img_bytes)

        # Display results
        st.markdown(f"""
        <div class='analysis-card'>
            <div class='analysis-title'>🔍 Analysis Results</div>
            <div class='result-item'>
                <span class='result-label'>🏷️ Detected Issue:</span>
                <span class='label-badge'>{result['label']}</span>
            </div>
            <div class='result-item'>
                <span class='result-label'>📊 Confidence Level:</span>
                <span class='confidence-badge'>{result['confidence']}%</span>
            </div>
            <div class='result-item'>
                <span class='result-label'>📝 Description:</span><br>
                {result['description']}
            </div>
            <div class='result-item'>
                <span class='result-label'>⚠️ Severity Level:</span>
                <span class='severity-badge'>{result['severity']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- Recommendations Section ---
    st.markdown("""
    <div class='recommendations-section'>
        <h3 class='recommendations-title'>🛠️ Maintenance Recommendations</h3>
    """, unsafe_allow_html=True)

    for i, rec in enumerate(result.get("recommendation", []), 1):
        st.markdown(f"""
        <div class='recommendation-item'>
            <strong>Step {i}:</strong> {rec}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # --- Service Centers Section ---
    centers = load_service_centers()
    matched = [c for c in centers if result["label"] in c["specialties"]]

    st.markdown("""
    <div class='service-centers-section'>
        <h3 class='service-centers-title'>📍 Find Nearby Service Centers</h3>
    """, unsafe_allow_html=True)

    # Location inputs
    st.markdown("<div class='location-inputs'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        user_lat = st.number_input("📍 Your Latitude", value=6.9271, step=0.01, format="%.4f")
    with col2:
        user_lon = st.number_input("📍 Your Longitude", value=79.8612, step=0.01, format="%.4f")
    st.markdown("</div>", unsafe_allow_html=True)

    user_location = (user_lat, user_lon)

    # Map and service centers
    map_col, list_col = st.columns([1.3, 1])

    with map_col:
        service_map = folium.Map(location=user_location, zoom_start=11)
        
        # Add user location
        folium.Marker(
            user_location, 
            tooltip="📍 Your Location", 
            popup="You are here",
            icon=folium.Icon(color="blue", icon="user", prefix="fa")
        ).add_to(service_map)

        # Add service centers
        for center in matched:
            coord = (center["latitude"], center["longitude"])
            dist_km = round(geodesic(user_location, coord).km, 2)
            popup_text = f"""
            <b>{center['name']}</b><br>
            📍 {center['address']}<br>
            📞 {center.get('contact', 'N/A')}<br>
            🚗 Distance: {dist_km} km<br>
            🔧 Specialties: {', '.join(center['specialties'])}
            """
            folium.Marker(
                coord, 
                tooltip=center["name"], 
                popup=popup_text,
                icon=folium.Icon(color="green", icon="wrench", prefix="fa")
            ).add_to(service_map)

        st_folium(service_map, height=400, width=None)

    with list_col:
        for center in matched[:5]:
            coord = (center["latitude"], center["longitude"])
            distance = round(geodesic(user_location, coord).km, 2)
            
            st.markdown(f"""
            <div class='service-center-card'>
                <div class='service-center-name'>{center['name']}</div>
                <div class='service-center-info'>📍 {center['address']}</div>
                <div class='service-center-info'>📞 {center.get('contact', 'Contact not available')}</div>
                <div class='service-center-info'>🔧 Specialties: {', '.join(center['specialties'])}</div>
                <div style='margin-top: 15px;'>
                    <span class='distance-badge'>📏 {distance} km away</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer-bar">
  <img src="https://img.icons8.com/fluency/32/car--v1.png" alt="AutoVision Logo" class="footer-logo"/>
  <span>AutoVision AI © 2025 – Vehicle Maintenance Predictor | All rights reserved</span>
</div>
""", unsafe_allow_html=True)

