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
st.subheader("Protect Your Network from Unauthorized Access 🚀")

st.write("Enter network connection details below to check for intrusions.")

st.markdown("<h4>Count</h4><p style='font-size:14px; color:gray;'>Number of connections to the same host in a short time.</p>", unsafe_allow_html=True)
count = st.number_input("Count", min_value=0, value=5)

st.markdown("<h4>Source Bytes</h4><p style='font-size:14px; color:gray;'>Data sent from source to destination (in bytes).</p>", unsafe_allow_html=True)
src_bytes = st.number_input("Source Bytes", min_value=0, value=500)

st.markdown("<h4>Logged In</h4><p style='font-size:14px; color:gray;'>Indicates whether the user is logged in (1 = Yes, 0 = No).</p>", unsafe_allow_html=True)
logged_in = st.selectbox("Logged In", [0, 1])

st.markdown("<h4>Service Error Rate</h4><p style='font-size:14px; color:gray;'>Percentage of connections that have SYN errors.</p>", unsafe_allow_html=True)
srv_serror_rate = st.number_input("Service Error Rate", min_value=0.0, max_value=1.0, value=0.2)

st.markdown("<h4>Destination Bytes</h4><p style='font-size:14px; color:gray;'>Data sent from destination to source (in bytes).</p>", unsafe_allow_html=True)
dst_bytes = st.number_input("Destination Bytes", min_value=0, value=1000)

st.markdown("<h4>Service Count</h4><p style='font-size:14px; color:gray;'>Number of connections to the same service.</p>", unsafe_allow_html=True)
srv_count = st.number_input("Service Count", min_value=0, value=10)


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
