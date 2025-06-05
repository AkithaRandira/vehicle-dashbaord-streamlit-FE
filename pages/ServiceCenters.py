import streamlit as st
import json
import os
import urllib.parse

# --- Constants ---
SERVICE_CENTERS_FILE = "service_centers.json"

# --- Load Service Centers ---
def load_service_centers():
    try:
        with open(SERVICE_CENTERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- Generate Google Maps URL ---
def get_google_maps_url(address):
    """Generate Google Maps URL for the given address"""
    encoded_address = urllib.parse.quote(address)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

# --- Generate Google Maps Embed URL ---
def get_google_maps_embed_url(address):
    """Generate Google Maps embed URL for the given address"""
    encoded_address = urllib.parse.quote(address)
    return f"https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q={encoded_address}"

# --- Streamlit Config ---
st.set_page_config(page_title="📍 Service Centers - AutoVision", layout="wide", initial_sidebar_state="collapsed")

# --- Navbar & Global Styles ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body, .stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 50%, #f8fafc 100%);
    color: #1e293b;
    padding-bottom: 100px;
}

#MainMenu, footer, header { visibility: hidden; }

.navbar {
    position: fixed; top: 0; left: 0; width: 100%;
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 48px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(25px);
    z-index: 999;
    border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}
.nav-brand { display: flex; align-items: center; gap: 12px; }
.nav-brand img { height: 32px; width: 32px; }
.brand-text {
    font-size: 26px; font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.beta-badge {
    background: #667eea; color: #fff; font-size: 10px;
    padding: 2px 8px; border-radius: 12px; font-weight: 700;
}
.nav-links { display: flex; gap: 24px; }
.nav-links a {
    text-decoration: none; font-size: 15px;
    padding: 8px 16px; border-radius: 8px; font-weight: 500;
    color: #64748b; transition: 0.3s ease;
}
.nav-links a:hover {
    background: rgba(102, 126, 234, 0.1); color: #667eea;
}
.nav-links a.active {
    background: linear-gradient(135deg, #667eea, #764ba2); color: white;
}

.page-header {
    margin-top: 10px; text-align: center;
    padding: 10px 20px 0;
}
.page-title {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-subtitle {
    font-size: 1rem; color: #6b7280;
    margin-top: 10px;
}

.search-container {
    max-width: 800px;
    margin: 30px auto;
    padding: 0 20px;
}

.filters-container {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    justify-content: center;
}
            /* Boost expander title visibility */
.streamlit-expanderHeader {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    padding: 12px 18px !important;
}

/* Add spacing between expanders */
.stExpander {
    margin-bottom: 16px !important;
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    box-shadow: 0 6px 12px rgba(102, 126, 234, 0.08) !important;
}

            .stExpander:hover {
    border-color: #667eea !important;
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15) !important;
    transform: translateY(-2px);
    transition: all 0.2s ease-in-out;
}


.filter-chip {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    padding: 8px 16px;
    border-radius: 25px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-chip:hover {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.filter-chip.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
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
    font-weight: 700; font-size: 1.2rem; color: #1f2937;
    margin-bottom: 10px;
}
.service-center-info {
    color: #6b7280;
    line-height: 1.6;
    margin-bottom: 5px;
}

.search-container {
    position: sticky;
    top: 80px;
    z-index: 100;
    background: #f8fafc;
    padding: 15px 25px;
    border-bottom: 1px solid #e2e8f0;
}
            

.map-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    margin-top: 15px;
    transition: all 0.3s ease;
}

.map-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    text-decoration: none;
    color: white;
}

.directions-button {
    background: #10b981;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    margin-top: 15px;
    margin-left: 10px;
    transition: all 0.3s ease;
}
            
            ::placeholder {
    color: #4b5563 !important; /* darker gray for better contrast */
    opacity: 1 !important;
    font-weight: 500;
}


.directions-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
    text-decoration: none;
    color: white;
}

.map-container {
    width: 100%;
    height: 300px;
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    margin-top: 15px;
    overflow: hidden;
}

.footer-bar {
    position: fixed;
    bottom: 0; left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    padding: 12px;
    text-align: center;
    font-size: 0.9rem;
    color: #64748b;
    border-top: 1px solid #e5e7eb;
    z-index: 1000;
}

.results-summary {
    text-align: center;
    color: #6b7280;
    font-size: 16px;
    margin: 20px 0;
    padding: 15px;
    background: rgba(102, 126, 234, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(102, 126, 234, 0.1);
}
</style>
<div class='navbar'>
    <div class='nav-brand'>
        <img src='https://img.icons8.com/fluency/48/car--v1.png'/>
        <div>
            <span class='brand-text'>AutoVision</span>
            <span class='beta-badge'>BETA</span>
        </div>
    </div>
    <div class='nav-links'>
    <a href="/" target="_self">🏠 Home</a>
    <a href="/History" target="_self">📊 History</a>
    <a href="/ServiceCenters" target="_self">📍 Service Centers</a>
    <a href="/Profile" target="_self">👤 Profile</a>
</div>

</div>
<br><br>

""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="page-header">
  <h1 class="page-title">📍 Service Centers</h1>
  <p class="page-subtitle">Search for specialized repair centers for your vehicle's needs.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Service Centers ---
centers = load_service_centers()

# --- Search and Filter Section ---
st.markdown('<div class="search-container">', unsafe_allow_html=True)

# Search input with better styling
st.markdown("""
<style>
.stTextInput > div > div > input {
    background-color: white;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 16px;
    color: #1f2937;
}
.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
.stTextInput > label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

search = st.text_input("🔍 Search by name, specialty or location:", "", key="search_box")

# Create columns for additional filters with better styling
st.markdown("""
<style>
.stSelectbox > label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
.stSelectbox > div > div {
    background-color: white;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
}
.stCheckbox > label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    specialty_filter = st.selectbox(
        "🔧 Filter by Specialty:",
        ["All Specialties"] + list(set([spec for center in centers for spec in center.get('specialties', [])]))
    )

with col2:
    location_filter = st.selectbox(
        "📍 Filter by Location:",
        ["All Locations"] + list(set([center.get('address', '').split(',')[-1].strip() for center in centers if center.get('address')]))
    )

with col3:
    show_map = st.checkbox("🗺️ Show Maps", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# --- Filter Logic ---
filtered = centers

# Apply search filter
if search:
    filtered = [c for c in filtered if search.lower() in json.dumps(c).lower()]

# Apply specialty filter
if specialty_filter != "All Specialties":
    filtered = [c for c in filtered if specialty_filter in c.get('specialties', [])]

# Apply location filter
if location_filter != "All Locations":
    filtered = [c for c in filtered if location_filter in c.get('address', '')]

# --- Results Summary ---
if filtered:
    st.markdown(f"""
    <div class="results-summary">
        📊 Found <strong>{len(filtered)}</strong> service center(s) matching your criteria
    </div>
    """, unsafe_allow_html=True)

# --- Display Service Centers ---
for i, center in enumerate(filtered):
    # Create expandable section for each service center
    with st.expander(f"🏢 {center['name']}", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class='service-center-card'>
                <div class='service-center-name'>{center['name']}</div>
                <div class='service-center-info'>📍 {center['address']}</div>
                <div class='service-center-info'>📞 {center.get('contact', 'Contact not available')}</div>
                <div class='service-center-info'>🔧 Specialties: {', '.join(center.get('specialties', []))}</div>
                <div class='service-center-info'>⭐ Rating: {center.get('rating', 'Not rated')} / 5</div>
                <div class='service-center-info'>🕒 Hours: {center.get('hours', 'Hours not available')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add buttons using Streamlit components with proper links
            col_btn1, col_btn2 = st.columns(2)
            maps_url = get_google_maps_url(center['address'])
            directions_url = f"https://www.google.com/maps/dir//{urllib.parse.quote(center['address'])}"
            
            with col_btn1:
                st.markdown(f"""
                <a href="{maps_url}" target="_blank" style="
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 14px;
                    text-align: center;
                    width: 100%;
                    box-sizing: border-box;
                    transition: all 0.3s ease;
                ">
                    🗺️ View on Maps
                </a>
                """, unsafe_allow_html=True)
                    
            with col_btn2:
                st.markdown(f"""
                <a href="{directions_url}" target="_blank" style="
                    display: inline-block;
                    background: #10b981;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 14px;
                    text-align: center;
                    width: 100%;
                    box-sizing: border-box;
                    transition: all 0.3s ease;
                ">
                    🧭 Get Directions
                </a>
                """, unsafe_allow_html=True)
        
        with col2:
            if show_map:
                # Display embedded map using st.components for better compatibility
                map_html = f"""
                <div class="map-container">
                    <iframe
                        width="100%"
                        height="300"
                        frameborder="0"
                        style="border:0; border-radius: 12px;"
                        src="https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dO3TdaYWBQ_uOg&q={urllib.parse.quote(center['address'])}"
                        allowfullscreen>
                    </iframe>
                </div>
                """
                st.markdown(map_html, unsafe_allow_html=True)
            else:
                # Show a placeholder or additional info
                st.markdown(f"""
                <div style="padding: 20px; text-align: center; color: #6b7280; background: #f8fafc; border-radius: 12px; border: 2px dashed #e2e8f0;">
                    <p>📍 <strong>Quick Access</strong></p>
                    <p>Enable "Show Maps" to view location</p>
                    <p style="font-size: 12px; margin-top: 15px;">
                        <strong>Services:</strong><br>
                        {', '.join(center.get('specialties', []))}
                    </p>
                </div>
                """, unsafe_allow_html=True)

# --- No Results Found ---
if not filtered:
    st.markdown("""
    <div style='text-align:center; margin-top:30px; color:#6b7280;'>
        <div style="font-size: 48px; margin-bottom: 20px;">🔍</div>
        <h3>No matching service centers found</h3>
        <p>Try adjusting your search criteria or filters</p>
        <div style="margin-top: 20px; padding: 20px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0;">
            <p><strong>Search Tips:</strong></p>
            <p>• Try broader search terms</p>
            <p>• Check different specialties</p>
            <p>• Clear location filters</p>
            <p>• Use partial matches (e.g., "brake" instead of "brake repair")</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- Footer ---
st.markdown("""
<div class="footer-bar">
  <img src="https://img.icons8.com/fluency/32/car--v1.png" style="height: 20px; vertical-align: middle;"/>
  AutoVision AI © 2025 – Vehicle Maintenance Predictor | All rights reserved
</div>
""", unsafe_allow_html=True)