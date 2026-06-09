import streamlit as st
import pandas as pd
import time
import requests
import base64
import os
from streamlit_lottie import st_lottie
from model import load_or_train_model, predict_message

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Harmful Message Detector",
    page_icon="🛡️",
    layout="wide"
)

# --- HELPER FUNCTIONS ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Lottie Assets
lottie_shield = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_0wf8reuz.json")
lottie_warning = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_TkwPts.json")
lottie_success = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fbawu9ol.json")

# Apply CSS with Base64 Background & FontAwesome
def apply_custom_css():
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)
    
    css_file = "assets/style.css"
    bg_file = "assets/police_animated.svg"
    
    if os.path.exists(css_file):
        with open(css_file) as f:
            css_content = f.read()
        
        # Inject base64 image if background exists
        if os.path.exists(bg_file):
            bg_base64 = get_base64_of_bin_file(bg_file)
            css_content = css_content.replace(
                'url("app/assets/police_animated.svg")', 
                f'url("data:image/svg+xml;base64,{bg_base64}")'
            )
            
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

apply_custom_css()

# --- MODEL INITIALIZATION ---
model = load_or_train_model()

# --- HEADER ---
st.markdown("""
<div style="text-align: center; padding: 1.5rem 0;">
    <h1 style="margin-bottom: 0;">🛡️ Harmful Message Detector</h1>
    <p style="color: #ffffff; font-size: 1.25rem; font-weight: 400; margin-top: 8px; letter-spacing: 0.5px; opacity: 0.9;">
        <i class="fa-solid fa-user-shield" style="margin-right: 5px;"></i> Protect message, protect people
    </p>
</div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('### <div class="icon-container"><i class="fa-solid fa-terminal panel-icon"></i></div> Input Console', unsafe_allow_html=True)
    st.markdown("Submit text data to analyze safe, spam, or abusive vectors.")
    
    user_input = st.text_area(
        "Message Content",
        placeholder="Type or paste the suspicious message here...",
        height=220,
        label_visibility="collapsed"
    )
    
    # Empty space for spacing
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    if st.button("🔍 SCANNING..."):
        if user_input.strip() == "":
            st.warning("⚠️ Input terminal empty. Please feed message data.")
        else:
            with st.spinner("Analyzing message vectors via NLP Classifier..."):
                time.sleep(1.2) # Real-time simulation delay
                result = predict_message(user_input, model)
                st.session_state['analysis_result'] = result
                st.session_state['input_text'] = user_input

with col2:
    if 'analysis_result' in st.session_state:
        result = st.session_state['analysis_result']
        prediction_class = result['class']
        
        st.markdown('### <div class="icon-container"><i class="fa-solid fa-chart-line panel-icon"></i></div> Diagnostics Output', unsafe_allow_html=True)
        
        # Display Progress Metrics
        st.markdown(f"**Safety Score:** `{result['safe_prob']:.1f}%`")
        st.progress(result['safe_prob'] / 100)
        
        st.markdown(f"**Abusive Index:** `{result['abusive_prob']:.1f}%`")
        st.progress(result['abusive_prob'] / 100)
        
        st.markdown(f"**Spam Index:** `{result['spam_prob']:.1f}%`")
        st.progress(result['spam_prob'] / 100)
        st.markdown("---")
        
        if prediction_class == "Abusive":
            if lottie_warning:
                st_lottie(lottie_warning, height=120, key="warning")
            st.markdown(f"<h2 style='color: #ef4444; margin: 0; font-size: 1.8rem;'><i class='fa-solid fa-triangle-exclamation'></i> DETECTED ABUSIVE CONTENT</h2>", unsafe_allow_html=True)
            st.error("🚨 **Threat Matrix Alert:** This message contains harmful, hateful, or abusive patterns. Recommendation: Flag and quarantine.")
            
        elif prediction_class == "Spam":
            if lottie_warning:
                st_lottie(lottie_warning, height=120, key="warning")
            st.markdown(f"<h2 style='color: #f97316; margin: 0; font-size: 1.8rem;'><i class='fa-solid fa-envelope-open-text'></i> DETECTED SPAM CONTENT</h2>", unsafe_allow_html=True)
            st.warning("⚠️ **Spam Matrix Alert:** This message resembles advertising, scams, phishing, or bulk messages. Recommendation: Block or ignore.")
            
        else:
            if lottie_success:
                st_lottie(lottie_success, height=120, key="success")
            st.markdown(f"<h2 style='color: #22c55e; margin: 0; font-size: 1.8rem;'><i class='fa-solid fa-circle-check'></i> SYSTEM APPROVED</h2>", unsafe_allow_html=True)
            st.success("🛡️ **System Status Safe:** Message passes the ML security filters. Suitable for user channels.")
            
    else:
        st.markdown('### <div class="icon-container"><i class="fa-solid fa-shield-halved panel-icon"></i></div> Patrol Monitor', unsafe_allow_html=True)
        if lottie_shield:
            st_lottie(lottie_shield, height=200, key="shield")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: 300;'><i class='fa-solid fa-radar'></i> Scanning grid active. Standby for input transmission...</p>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; color: #64748b; margin-top: 5rem; padding-bottom: 2rem;">
    <p style="font-size: 0.9rem;"><i class="fa-solid fa-microchip"></i> CyberGuard Pipeline Engine v1.3.0 • Logistic Regression Vectorizer</p>
</div>
""", unsafe_allow_html=True)
