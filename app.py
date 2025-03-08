import streamlit as st
import numpy as np
import pickle

# Load the trained model
model_path = "model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Streamlit UI
st.title("🔍 Intrusion Detection System (IDS)")
st.write("This app predicts whether a network connection is an **Intrusion (Attack) or Normal**.")

# Input fields
st.sidebar.header("Enter Network Connection Features")

# User input fields
feature_values = []
for i in range(32):  # Assuming 32 features
    value = st.sidebar.number_input(f"Feature {i+1}", value=0.0)
    feature_values.append(value)

# Convert input to numpy array
input_data = np.array(feature_values).reshape(1, -1)

# Prediction
if st.button("Detect Intrusion"):
    prediction = model.predict(input_data)
    if prediction == 1:
        st.error("🚨 Intrusion Detected! (Malicious Connection)")
    else:
        st.success("✅ Normal Connection (Safe)")

