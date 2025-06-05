import streamlit as st
import json
from datetime import datetime
import os
import base64

# --- Constants ---
HISTORY_FILE = "history.json"

# --- Load History ---
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- Format Timestamp ---
def format_timestamp(ts):
    return datetime.fromisoformat(ts).strftime("%B %d, %Y")

# --- Process Image Data ---
def process_image_data(image_data):
    if not image_data:
        return None
    if image_data.startswith("data:image/"):
        return image_data
    return f"data:image/jpeg;base64,{image_data}"

# --- Streamlit Config ---
st.set_page_config(page_title="📊 Analysis History - AutoVision", layout="wide", initial_sidebar_state="collapsed")

# --- Global Styles + Navbar ---
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
.nav-brand {
    display: flex; align-items: center; gap: 12px;
}
.nav-brand img {
    height: 32px; width: 32px;
}
.brand-text {
    font-size: 26px; font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.beta-badge {
    background: #667eea;
    color: #fff;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 12px;
    font-weight: 700;
}
.nav-links {
    display: flex; gap: 24px;
}
.nav-links a {
    text-decoration: none;
    font-size: 15px;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 500;
    color: #64748b;
    transition: 0.3s ease;
}
.nav-links a:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
}
.nav-links a.active {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

.page-header {
    margin-top: 5px;
    text-align: center;
    padding: 5px 5px 0;
}
.page-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-subtitle {
    font-size: 1rem;
    color: #6b7280;
    margin-top: 10px;
}

.record-card {
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    margin: 20px 0;
    padding: 30px;
    border-left: 6px solid #667eea;
}
.record-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 15px;
}
.record-title {
    font-size: 1.4rem;
    font-weight: 700;
}
.record-date {
    font-size: 0.9rem;
    color: #6b7280;
}
.record-sub {
    margin: 20px 0;
    font-weight: 500;
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
    padding: 12px 16px;
    border-radius: 12px;
}
.record-tags {
    display: flex; gap: 10px; flex-wrap: wrap;
}
.tag {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}
.record-content {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.record-image {
    max-width: 280px;
    max-height: 280px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    object-fit: cover;
}
.recommendations-section {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #e5e7eb;
}
.recommendations-title {
    font-weight: 700;
    color: #16a34a;
    margin-bottom: 10px;
}
.recommendation-item {
    background: #f0fdf4;
    color: #166534;
    padding: 8px 12px;
    border-left: 3px solid #22c55e;
    border-radius: 10px;
    margin-bottom: 8px;
}
button[kind="primary"], button[kind="secondary"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    font-weight: 600;
    border: none;
    border-radius: 12px;
    padding: 8px 16px;
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
<br><br><br>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="page-header">
  <h1 class="page-title">📊 Analysis History</h1>
  <p class="page-subtitle">Review past vehicle dashboard predictions and maintenance suggestions.</p>
</div>
""", unsafe_allow_html=True)

# --- Clear History ---
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🗑 Clear All History"):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            st.rerun()

# --- Load & Render History ---
history = load_history()
if history:
    st.markdown(f"<p style='color:#6b7280;'>📋 Found {len(history)} analysis record{'s' if len(history)!=1 else ''}</p>", unsafe_allow_html=True)
    for entry in history:
        timestamp = format_timestamp(entry["timestamp"])
        tags = ''.join([f"<span class='tag'>{label}</span>" for label in entry.get("labels", [])])
        recommendations = ''.join([f"<div class='recommendation-item'>• {rec}</div>" for rec in entry.get("recommendations", [])])

        image_data = process_image_data(entry.get("image", ""))
        image_html = f'<img src="{image_data}" class="record-image" />' if image_data else '<div style="color:#999">Image not available</div>'

        st.markdown(f"""
        <div class='record-card'>
            <div class='record-header'>
                <div class='record-title'>Analysis Report</div>
                <div class='record-date'>📅 {timestamp}</div>
            </div>
            <div class='record-sub'>
                ⚠️ <strong>Detected Issues:</strong> {', '.join(entry.get("labels", ["No issues detected"]))}
            </div>
            <div class='record-content'>
                <div style='flex: 1; min-width: 300px;'>
                    <div class='record-tags'>{tags}</div>
                    <div class='recommendations-section'>
                        <div class='recommendations-title'>💡 AI Recommendations</div>
                        {recommendations if recommendations else "<div class='recommendation-item'>• No specific recommendations available</div>"}
                    </div>
                </div>
                <div style='flex-shrink: 0;'>
                    {image_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='record-card'>
        <div style='text-align: center; padding: 60px; color: #6b7280;'>
            <h3 style='margin-bottom: 10px;'>No Analysis History Found</h3>
            <p>Start by uploading and analyzing your dashboard image on the home page.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer-bar">
  <img src="https://img.icons8.com/fluency/32/car--v1.png" style="height: 20px; vertical-align: middle;"/>
  AutoVision AI © 2025 – Intelligent Vehicle Maintenance Predictor | All rights reserved
</div>
""", unsafe_allow_html=True)
