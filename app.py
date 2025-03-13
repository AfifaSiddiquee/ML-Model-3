# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the pre-trained ML model (ensure you have this file saved in your project)
model = pickle.load(open("model.pkl", "rb"))

# --- Page Setup ---
st.set_page_config(page_title="Machine Learning Intrusion Detection System", layout="wide")

# --- Custom CSS for styling ---
st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem; }
    .title { font-size: 2rem; font-weight: bold; }
    .description { color: #555; font-size: 1rem; margin-bottom: 1.5rem; }
    .stButton > button { background-color: #4CAF50; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Page Navigation State ---
if "page" not in st.session_state:
    st.session_state.page = 1


# --- Function for navigating pages ---
def next_page():
    st.session_state.page += 1


def prev_page():
    st.session_state.page -= 1


# --- Prediction Function ---
def predict_intrusion(features):
    # Convert inputs into DataFrame for model
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)
    return "Intrusion Detected" if prediction[0] == 1 else "Normal Traffic"


# --- Page 1: About the App ---
if st.session_state.page == 1:
    st.title("📖 About the IDS App")
    st.markdown(
        """
        🔹 **Machine Learning-based Intrusion Detection System (IDS)**  
        🔹 **Identifies malicious network traffic to protect networks**  
        
        ### How to use:
        1️⃣ **Read this description**  
        2️⃣ **Enter network details on the next page**  
        3️⃣ **Get a prediction: Normal 🔵 or Intrusion 🔴**  
        """
    )

    if st.button("Next ➡️"):
        next_page()


# --- Page 2: Enter Network Details ---
if st.session_state.page == 2:
    # Force the title to stick to the top
    st.markdown("<h1 class='title'>🔧 Enter Network Details</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Fill in the following details to predict potential intrusions:</p>", unsafe_allow_html=True)

    # Input fields setup
    fields = [
        ("Count", "Number of connections to the same host in a short time.", st.number_input, {"min_value": 0, "value": 5, "key": "count"}),
        ("Source Bytes", "Data sent from source to destination (in bytes).", st.number_input, {"min_value": 0, "value": 500, "key": "src_bytes"}),
        ("Logged In", "User logged in? (1 = Yes, 0 = No)", st.selectbox, {"options": [0, 1], "key": "logged_in"}),
        ("Service Error Rate", "Percentage of connections with errors.", st.number_input, {"min_value": 0.0, "max_value": 1.0, "value": 0.2, "key": "srv_serror_rate"}),
        ("Destination Bytes", "Data sent from destination to source.", st.number_input, {"min_value": 0, "value": 1000, "key": "dst_bytes"}),
        ("Service Count", "Number of connections to the same service.", st.number_input, {"min_value": 0, "value": 10, "key": "srv_count"}),
    ]

    # Display inputs with descriptions
    for feature, description, input_type, kwargs in fields:
        st.markdown(f"**{feature}:**")
        st.markdown(f"<p style='font-size:12px; color:#555; margin-top:-5px;'>{description}</p>", unsafe_allow_html=True)
        input_type("", **kwargs)

    # "Back" button for navigation
    if st.button("⬅️ Back"):
        prev_page()

    # Intrusion Detection Button
    if st.button("🔍 Detect Intrusion"):
        # Collect input data from fields
        input_data = {field[0].lower().replace(" ", "_"): st.session_state[field[3]["key"]] for field in fields}
        result = predict_intrusion(input_data)

        # Display result with color
        if "Intrusion" in result:
            st.error(f"🚨 **{result}** 🚨")
        else:
            st.success(f"✅ **{result}**")
