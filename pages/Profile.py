import streamlit as st

# --- Streamlit Config ---
st.set_page_config(page_title="👤 Profile - AutoVision", layout="wide", initial_sidebar_state="collapsed")

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
    margin-top: 20px;
    text-align: center;
    padding: 0 20px 0;
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
    color: #4b5563;
    margin-top: 8px;
}
.profile-card {
    max-width: 600px;
    background: white;
    margin: 40px auto;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    border-left: 6px solid #667eea;
}
.profile-card h3 {
    margin-bottom: 10px;
    font-size: 1.4rem;
    color: #1e293b;
}
.profile-card p {
    color: #475569;
    font-size: 0.95rem;
    margin-bottom: 8px;
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
<br><br>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="page-header">
  <h1 class="page-title">👤 User Profile</h1>
  <p class="page-subtitle">Manage your preferences and explore your account details.</p>
</div>
""", unsafe_allow_html=True)

# --- Profile Content ---
st.markdown("""
<div class="profile-card">
  <h3>👨‍💼 Name:</h3>
  <p>John Doe</p>

  <h3>📧 Email:</h3>
  <p>johndoe@example.com</p>

  <h3>🚗 Preferred Vehicle:</h3>
  <p>Toyota Corolla 2021</p>

  <h3>📍 Location:</h3>
  <p>Colombo, Sri Lanka</p>

  <h3>🔐 Account Settings:</h3>
  <p><em>(Settings panel coming soon...)</em></p>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer-bar">
  <img src="https://img.icons8.com/fluency/32/car--v1.png" style="height: 20px; vertical-align: middle;"/>
  AutoVision AI © 2025 – Vehicle Maintenance Predictor | All rights reserved
</div>
""", unsafe_allow_html=True)
