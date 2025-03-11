import streamlit as st
import pandas as pd
import joblib

# Load trained model and scaler
model = joblib.load("intrusion_detection_model.pkl")
scaler = joblib.load("scaler.pkl")

# Define function for prediction
def predict_intrusion(data):
    # Convert input data to DataFrame
    df = pd.DataFrame([data])

    # Ensure all features exist
    for col in X_train.columns:
        if col not in df:
            df[col] = 0

    # Reorder columns
    df = df[X_train.columns]

    # Scale the data
    df_scaled = scaler.transform(df)

    # Predict
    prediction = model.predict(df_scaled)
    return "🔵 Normal Connection" if prediction[0] == 0 else "🔴 Intrusion Detected (Attack!)"

# Streamlit UI
st.title("🔍 Intrusion Detection System")
st.write("Enter network connection details to check for intrusions.")

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
