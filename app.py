import streamlit as st
import pandas as pd
import joblib

# Load trained model, scaler, and feature names
model = joblib.load("intrusion_detection_model.pkl")
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")  # Load saved feature names

# Define function for prediction
def predict_intrusion(data):
    # Convert input data to DataFrame
    df = pd.DataFrame([data])

    # Ensure all features exist
    for col in feature_names:  # Use loaded feature names instead of X_train.columns
        if col not in df:
            df[col] = 0

    # Reorder columns
    df = df[feature_names]

    # Scale the data
    df_scaled = scaler.transform(df)

    # Predict
    prediction = model.predict(df_scaled)
    return "🔵 Normal Connection" if prediction[0] == 0 else "🔴 Intrusion Detected (Attack!)"

# Add a sidebar for more details
st.sidebar.title("📖 About the IDS App")
st.sidebar.write("""
🔹 **This is a Machine Learning-based Intrusion Detection System (IDS).**  
🔹 It helps identify **malicious network traffic** and **protects networks from attacks.**  
🔹 **How to use:**  
&nbsp;&nbsp;&nbsp; 1️⃣ Enter network details in the main panel.  
&nbsp;&nbsp;&nbsp; 2️⃣ Click **"Detect Intrusion"** to analyze the connection.  
&nbsp;&nbsp;&nbsp; 3️⃣ The app will classify it as **Normal (Safe) 🔵** or **Intrusion (Attack!) 🔴**.  
""")

st.title("🔍 Intrusion Detection System")
st.subheader("Protect Your Network from Unauthorized Access")

# Define styling for feature names
feature_style = "<p style='font-size:16px; font-weight:bold; margin-bottom:5px;'>"

# Use columns to align labels and input boxes
col1, col2 = st.columns([2, 3])  # Adjust column widths as needed

with col1:
    st.markdown(f"{feature_style}Count:</p>", unsafe_allow_html=True)
with col2:
    count = st.number_input("", min_value=0, value=5, key="count")

with col1:
    st.markdown(f"{feature_style}Source Bytes:</p>", unsafe_allow_html=True)
with col2:
    src_bytes = st.number_input("", min_value=0, value=500, key="src_bytes")

with col1:
    st.markdown(f"{feature_style}Logged In:</p>", unsafe_allow_html=True)
with col2:
    logged_in = st.selectbox("", [0, 1], key="logged_in")

with col1:
    st.markdown(f"{feature_style}Service Error Rate:</p>", unsafe_allow_html=True)
with col2:
    srv_serror_rate = st.number_input("", min_value=0.0, max_value=1.0, value=0.2, key="srv_serror_rate")

with col1:
    st.markdown(f"{feature_style}Destination Bytes:</p>", unsafe_allow_html=True)
with col2:
    dst_bytes = st.number_input("", min_value=0, value=1000, key="dst_bytes")

with col1:
    st.markdown(f"{feature_style}Service Count:</p>", unsafe_allow_html=True)
with col2:
    srv_count = st.number_input("", min_value=0, value=10, key="srv_count")

# Predict button
if st.button("🔍 Detect Intrusion"):
    # Prepare data for prediction
    input_data = {
        "count": count,
        "src_bytes": src_bytes,
        "logged_in": logged_in,
        "srv_serror_rate": srv_serror_rate,
        "dst_bytes": dst_bytes,
        "srv_count": srv_count
    }
    
    # Get prediction
    result = predict_intrusion(input_data)
    
    # Show result
    st.success(f"**Prediction: {result}**")
