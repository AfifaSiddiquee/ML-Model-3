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

# Add another section in the sidebar for feature explanations
st.sidebar.header("📌 Feature Descriptions")
st.sidebar.write("""
🔹 **Count:** Number of connections to the same host in a short time.  
🔹 **Source Bytes:** Data sent from source to destination.  
🔹 **Logged In:** Whether the user is logged in (1 = Yes, 0 = No).  
🔹 **Service Error Rate:** Percentage of connections that have errors.  
🔹 **Destination Bytes:** Data sent from destination to source.  
🔹 **Service Count:** Number of connections to the same service.  
""")

# Add a contact/info section
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ More Information")
st.sidebar.write("🔗 Visit [Streamlit Docs](https://docs.streamlit.io/) for more about Streamlit apps!")


# User input fields
count = st.number_input("Count", min_value=0, value=5)
src_bytes = st.number_input("Source Bytes", min_value=0, value=500)
logged_in = st.selectbox("Logged In", [0, 1])
srv_serror_rate = st.number_input("Service Error Rate", min_value=0.0, max_value=1.0, value=0.2)
dst_bytes = st.number_input("Destination Bytes", min_value=0, value=1000)
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
