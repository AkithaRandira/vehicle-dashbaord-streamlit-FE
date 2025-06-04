import streamlit as st
import json
from datetime import datetime
import pandas as pd
import os

# --- Constants ---
HISTORY_FILE = "history.json"

# --- Load Functions ---
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def format_timestamp(ts):
    return datetime.fromisoformat(ts).strftime("%b %d, %Y")

def get_relative_time(ts):
    now = datetime.now()
    past = datetime.fromisoformat(ts)
    diff = now - past
    
    if diff.days == 0:
        return "Today"
    elif diff.days == 1:
        return "1 day ago"
    elif diff.days < 30:
        return f"{diff.days} days ago"
    elif diff.days < 365:
        months = diff.days // 30
        return f"about {months} month{'s' if months > 1 else ''} ago"
    else:
        years = diff.days // 365
        return f"about {years} year{'s' if years > 1 else ''} ago"

# --- Streamlit Config ---
st.set_page_config(page_title="Analysis History", layout="wide")

# --- Dark Theme Styles ---
st.markdown("""
<style>
/* Dark theme background */
.stApp {
    background-color: #0f1419 !important;
}

.main .block-container {
    background-color: #0f1419 !important;
    padding-top: 2rem;
}

/* Main header styling */
.main-header {
    font-size: 2.5em;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* Clear button styling */
.clear-history-btn {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.9em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.clear-history-btn:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

/* Section containers */
.records-section {
    background: linear-gradient(145deg, #1a1f2e, #161b26);
    border-radius: 16px;
    padding: 0;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid #2d3748;
    overflow: hidden;
}

.details-section {
    background: linear-gradient(145deg, #1a1f2e, #161b26);
    border-radius: 16px;
    padding: 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid #2d3748;
    overflow: hidden;
    min-height: 400px;
}

/* Section headers */
.section-header {
    background: linear-gradient(135deg, #2d3748, #2a2f3a);
    padding: 25px 30px;
    border-bottom: 1px solid #4a5568;
}

.section-title {
    font-size: 1.4em;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.section-subtitle {
    color: #a0aec0;
    font-size: 0.95em;
    margin: 8px 0 0 0;
}

/* Table styling */
.table-header {
    background: linear-gradient(135deg, #2a2f3a, #252a35);
    padding: 20px 30px;
    border-bottom: 1px solid #4a5568;
    display: grid;
    grid-template-columns: 1.2fr 100px 2fr 1fr;
    gap: 25px;
    align-items: center;
    font-weight: 700;
    color: #e2e8f0;
    font-size: 0.95em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.table-row {
    padding: 25px 30px;
    border-bottom: 1px solid #2d3748;
    display: grid;
    grid-template-columns: 1.2fr 100px 2fr 1fr;
    gap: 25px;
    align-items: center;
    transition: all 0.3s ease;
    background: rgba(26, 31, 46, 0.5);
}

.table-row:hover {
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.6), rgba(42, 47, 58, 0.6));
    transform: translateX(5px);
    border-left: 4px solid #3b82f6;
}

.table-row:last-child {
    border-bottom: none;
}

/* Date styling */
.date-main {
    font-weight: 600;
    color: #ffffff;
    font-size: 1em;
    margin-bottom: 4px;
}

.date-relative {
    color: #718096;
    font-size: 0.85em;
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 400;
}

.date-icon {
    color: #4299e1;
    font-size: 0.9em;
}

/* Image styling */
.dashboard-image {
    width: 70px;
    height: 70px;
    border-radius: 12px;
    object-fit: cover;
    border: 2px solid #4a5568;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.dashboard-image:hover {
    transform: scale(1.05);
    border-color: #3b82f6;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

/* Warning badges */
.warning-lights {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.warning-badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.warning-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.warning-badge.abs {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    color: white;
}

.warning-badge.oil-pressure {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
}

.warning-badge.engine-light {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
}

.warning-badge.battery-warning {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: white;
}

/* Action buttons */
.action-btn {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 0.9em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.action-btn:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.action-btn.hide {
    background: linear-gradient(135deg, #6b7280, #4b5563);
}

.action-btn.hide:hover {
    background: linear-gradient(135deg, #4b5563, #374151);
}

/* Details panel content */
.details-content {
    padding: 30px;
    color: #e2e8f0;
}

.details-image {
    width: 100%;
    max-width: 100%;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    border: 2px solid #4a5568;
}

.warning-section, .recommendations-section {
    margin-bottom: 25px;
}

.section-label {
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    font-size: 1.1em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.warning-list, .recommendation-list {
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.6), rgba(42, 47, 58, 0.6));
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #3b82f6;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
}

.warning-item, .recommendation-item {
    color: #cbd5e0;
    margin-bottom: 8px;
    font-size: 0.95em;
    line-height: 1.5;
}

.warning-item:last-child, .recommendation-item:last-child {
    margin-bottom: 0;
}

/* Empty states */
.empty-state {
    text-align: center;
    padding: 80px 20px;
    color: #718096;
}

.empty-state-icon {
    font-size: 4em;
    margin-bottom: 20px;
    opacity: 0.7;
}

.empty-state h3 {
    color: #e2e8f0;
    font-size: 1.3em;
    margin-bottom: 10px;
}

.empty-state p {
    color: #a0aec0;
    font-size: 1em;
}

.select-prompt {
    text-align: center;
    padding: 60px 20px;
    color: #718096;
}

.select-prompt-icon {
    font-size: 3em;
    margin-bottom: 20px;
    opacity: 0.7;
}

/* Responsive design */
@media (max-width: 768px) {
    .table-header, .table-row {
        grid-template-columns: 1fr;
        gap: 15px;
        padding: 20px;
    }
    
    .main-header {
        font-size: 2em;
    }
    
    .records-section, .details-section {
        margin-bottom: 15px;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #2d3748;
}

::-webkit-scrollbar-thumb {
    background: #4a5568;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #718096;
}
</style>
""", unsafe_allow_html=True)

# --- Page Header ---
col_header, col_clear = st.columns([3, 1])

with col_header:
    st.markdown('<h1 class="main-header">📊 Analysis History</h1>', unsafe_allow_html=True)

with col_clear:
    if st.button("🗑 Clear History", key="clear_btn", help="Clear all analysis history"):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            st.rerun()

# --- Load History ---
history = load_history()
if "selected_index" not in st.session_state:
    st.session_state.selected_index = -1

# --- Main Layout ---
col_main, col_details = st.columns([2.2, 1.3])

with col_main:
    # Records Section
    st.markdown("""
    <div class="records-section">
        <div class="section-header">
            <div class="section-title">🚗 Vehicle Analysis Records</div>
            <div class="section-subtitle">Complete history of your dashboard image analyses</div>
        </div>
    """, unsafe_allow_html=True)
    
    if history:
        # Table Header
        st.markdown("""
        <div class="table-header">
            <div>📅 Date</div>
            <div>🖼️ Image</div>
            <div>⚠️ Warning Lights</div>
            <div>🔧 Actions</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Table Rows
        for i, entry in enumerate(history):
            date_main = format_timestamp(entry["timestamp"])
            date_relative = get_relative_time(entry["timestamp"])
            
            # Create warning badges
            warning_badges = []
            for label in entry["labels"]:
                badge_class = label.lower().replace(" ", "-")
                warning_badges.append(f'<span class="warning-badge {badge_class}">{label}</span>')
            warning_lights_html = "".join(warning_badges)
            
            # Action button state
            is_selected = st.session_state.selected_index == i
            button_text = "Hide Details" if is_selected else "View Details"
            
            # Table row
            st.markdown(f"""
            <div class="table-row">
                <div>
                    <div class="date-main">{date_main}</div>
                    <div class="date-relative">
                        <span class="date-icon">🕒</span>{date_relative}
                    </div>
                </div>
                <div>
                    <img src="data:image/png;base64,{entry['image']}" class="dashboard-image" alt="Dashboard Image">
                </div>
                <div class="warning-lights">
                    {warning_lights_html}
                </div>
                <div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action button
            if st.button(button_text, key=f"btn_{i}", help=f"{'Hide' if is_selected else 'Show'} analysis details"):
                st.session_state.selected_index = -1 if is_selected else i
                st.rerun()
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📈</div>
            <h3>No Analysis History Found</h3>
            <p>Your dashboard analysis records will appear here once you start analyzing vehicle images.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_details:
    # Details Section
    st.markdown("""
    <div class="details-section">
        <div class="section-header">
            <div class="section-title">🔍 Analysis Details</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_index != -1 and history:
        entry = history[st.session_state.selected_index]
        warning_count = len(entry["labels"])
        
        st.markdown(f"""
        <div class="details-content">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="color: #a0aec0; font-size: 0.9em; margin-bottom: 5px;">
                    📅 {format_timestamp(entry['timestamp'])}
                </div>
                <div style="color: #4299e1; font-size: 0.85em; font-weight: 600;">
                    {warning_count} Warning Light{'s' if warning_count != 1 else ''} Detected
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display image
        st.image(f"data:image/png;base64,{entry['image']}", use_column_width=True)
        
        # Warning Lights Section
        st.markdown("""
        <div class="warning-section">
            <div class="section-label">⚠️ Warning Lights</div>
            <div class="warning-list">
        """, unsafe_allow_html=True)
        
        warning_badges = []
        for label in entry["labels"]:
            badge_class = label.lower().replace(" ", "-")
            warning_badges.append(f'<span class="warning-badge {badge_class}">{label}</span>')
        
        st.markdown(f'<div class="warning-lights">{"".join(warning_badges)}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Recommendations Section
        if entry.get("recommendations"):
            st.markdown("""
            <div class="recommendations-section">
                <div class="section-label">💡 Recommendations</div>
                <div class="recommendation-list">
            """, unsafe_allow_html=True)
            
            for rec in entry["recommendations"]:
                st.markdown(f'<div class="recommendation-item">• {rec}</div>', unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="select-prompt">
            <div class="select-prompt-icon">👆</div>
            <div style="color: #e2e8f0; font-size: 1.1em; margin-bottom: 10px; font-weight: 600;">
                Select Analysis Record
            </div>
            <p style="color: #a0aec0;">Choose an entry from the table above to view detailed analysis information and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)