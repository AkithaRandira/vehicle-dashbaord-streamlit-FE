import streamlit as st
import json
from datetime import datetime

# --- Constants ---
HISTORY_FILE = "history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def format_timestamp(ts):
    return datetime.fromisoformat(ts).strftime("%b %d, %Y")

# --- Streamlit Page Config ---
st.set_page_config(page_title="Analysis History", layout="wide")

# --- Custom Styles ---
st.markdown("""
<style>
.history-row:hover {
    background-color: #e5f0ff;
    cursor: pointer;
}
.badge {
    background-color: #2563eb;
    color: white;
    padding: 3px 8px;
    border-radius: 20px;
    font-size: 0.8em;
    margin-right: 5px;
    display: inline-block;
}
.container-box {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.03);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown("""
## 📄 Analysis History
<p style='color: gray;'>A list of past dashboard image analyses.</p>
""", unsafe_allow_html=True)

# --- History Display ---
history = load_history()
if "selected_index" not in st.session_state:
    st.session_state.selected_index = -1

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Vehicle Analysis Records")
    for i, entry in enumerate(history):
        label_str = " ".join([f"<span class='badge'>{lbl}</span>" for lbl in entry["labels"]])
        timestamp_str = format_timestamp(entry["timestamp"])

        with st.container():
            if st.button(f"{'Hide' if st.session_state.selected_index == i else 'View'} Details", key=f"btn_{i}"):
                st.session_state.selected_index = -1 if st.session_state.selected_index == i else i

            st.markdown(f"""
            <div class='container-box'>
                <b>{timestamp_str}</b><br>
                {label_str}
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("### Analysis Details")
    if st.session_state.selected_index != -1:
        entry = history[st.session_state.selected_index]
        st.image(entry["image"], width=350)
        st.markdown(f"**Date:** {format_timestamp(entry['timestamp'])}")
        st.markdown("**Warning Lights Detected:**")
        for label in entry["labels"]:
            st.markdown(f"- {label}")
        st.markdown("**Recommendations:**")
        for rec in entry.get("recommendations", []):
            st.markdown(f"- {rec}")
    else:
        st.info("Select an entry to view detailed information")
