import streamlit as st
from PIL import Image
import tempfile
from inference import predict_warning_light

st.set_page_config(page_title="Vehicle Maintenance Predictor", layout="wide")

# --- Hero Section ---
st.markdown("""
<div style='text-align: center; padding-top: 30px;'>
    <h1 style='font-size: 3em; color: #2563eb;'>Predict Vehicle Maintenance Before Issues Arise</h1>
    <p style='font-size: 1.2em;'>Upload your dashboard image and get early maintenance predictions using our advanced AI technology</p>
    <a href="#upload"><button style='padding: 10px 20px; background-color: #2563eb; color: white; border-radius: 8px;'>Get Started →</button></a>
    <a href="#history"><button style='padding: 10px 20px; background-color: white; color: #2563eb; border: 1px solid #2563eb; border-radius: 8px;'>View History</button></a>
</div>
""", unsafe_allow_html=True)

# --- Two-Column Layout: How It Works + Upload ---
st.markdown("<h2 style='padding-top: 60px;'></h2>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

# Left: How It Works
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

# Right: Upload Box
with col2:
    st.markdown("<h3 id='upload'>Upload Dashboard Image</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📤 Drag and drop or click to upload (JPG, PNG)", type=["jpg", "jpeg", "png"])

# --- If Uploaded, Run Inference ---
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        img_path = tmp_file.name

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(Image.open(img_path), caption="Uploaded Image", use_container_width=True)

    with col2:
        with st.spinner("Analyzing dashboard image..."):
            result = predict_warning_light(img_path)

        # --- Results Section ---
        st.markdown(f"""
        <div style='border: 1px solid #333; padding: 20px; border-radius: 10px; background-color: #1e1e1e; color: #f1f1f1; margin-top: 20px;'>
            <h3 style='color: #60a5fa;'>🔍 Analysis Results</h3>
            <p><strong>🔧 Label:</strong> <span style='background-color:#166534; color:#dcfce7; padding: 4px 10px; border-radius: 4px;'>{result['label']}</span></p>
            <p><strong>📊 Confidence:</strong> <span style='color:#facc15;'>{result['confidence']}%</span></p>
            <p><strong>📄 Description:</strong> {result['description']}</p>
            <p><strong>🚨 Severity:</strong> <span style='background-color:#7f1d1d; color:#fee2e2; padding: 4px 10px; border-radius: 4px;'>{result['severity']}</span></p>
        </div>
        """, unsafe_allow_html=True)

        # --- Dynamic Maintenance Recommendations ---
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
            

# --- Placeholder for History Section ---
st.markdown("""
<div id='history' style='margin-top: 100px;'>
    <h2>📜 Analysis History</h2>
    <p style='color: gray;'>This section will show a list of past dashboard analyses (coming soon).</p>
</div>
""", unsafe_allow_html=True)



