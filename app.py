# Import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the pre-trained ML model
model = pickle.load(open("intrusion_detection_model.pkl", "rb"))

# --- Set page configuration ---
st.set_page_config(page_title="Intrusion Detection System", layout="wide")

# --- Custom styling ---
st.markdown(
    """
    <style>
    .title { font-size: 2rem; font-weight: bold; color: #4A90E2; }
    .description { color: #555; font-size: 1rem; margin-bottom: 1rem; }
    .stButton > button { background-color: #4CAF50; color: white; font-weight: bold; }
    .input-label { font-size: 1.1rem; font-weight: bold; margin-top: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Page navigation setup ---
if "page" not in st.session_state:
    st.session_state.page = 1


# --- Page navigation functions ---
def next_page():
    st.session_state.page += 1


def prev_page():
    st.session_state.page -= 1


# --- Prediction function ---
def predict_intrusion(features):
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)
    return "🚨 Intrusion Detected!" if prediction[0] == 1 else "✅ Normal Traffic"


# --- Page 1: About the IDS App ---
if st.session_state.page == 1:
    st.title("📖 About the IDS App")
    st.markdown(
        """
        🔹 **Machine Learning-based Intrusion Detection System (IDS)**  
        🔹 **Detects malicious network traffic to protect your network**  
        
        ### How to use:
        1️⃣ **Read this overview**  
        2️⃣ **Enter network details on the next page**  
        3️⃣ **Get a prediction: Normal ✅ or Intrusion 🚨**  
        """
    )

    if st.button("Next ➡️"):
        next_page()


# --- Page 2: Enter Network Details ---
if st.session_state.page == 2:
    # Force the title to stay at the top
    st.markdown("<h1 class='title'>🔧 Enter Network Details</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Fill in the details below to predict potential intrusions:</p>", unsafe_allow_html=True)

    # --- Input fields setup ---
    col1, col2 = st.columns(2)

    with col1:
        count = st.number_input("🔹 Count", min_value=0, value=5, help="Number of connections to the same host in a short time.")
        source_bytes = st.number_input("🔹 Source Bytes", min_value=0, value=500, help="Data sent from source to destination (in bytes).")
        logged_in = st.selectbox("🔹 Logged In", [0, 1], help="User logged in? (1 = Yes, 0 = No)")

    with col2:
        service_error_rate = st.number_input("🔹 Service Error Rate", min_value=0.0, max_value=1.0, value=0.2, help="Percentage of connections with errors.")
        destination_bytes = st.number_input("🔹 Destination Bytes", min_value=0, value=1000, help="Data sent from destination to source.")
        service_count = st.number_input("🔹 Service Count", min_value=0, value=10, help="Number of connections to the same service.")

    # "Back" button for navigation
    if st.button("⬅️ Back"):
        prev_page()

    # Intrusion Detection button
    if st.button("🔍 Detect Intrusion"):
        # Gather user input data
        features = {
            "count": count,
            "source_bytes": source_bytes,
            "logged_in": logged_in,
            "service_error_rate": service_error_rate,
            "destination_bytes": destination_bytes,
            "service_count": service_count,
        }

        # Get prediction result
        result = predict_intrusion(features)

        # Display prediction result
        if "Intrusion" in result:
            st.error(f"🚨 **{result}** 🚨")
        else:
            st.success(f"✅ **{result}**")


