import streamlit as st
import pandas as pd
import joblib

# Load model, scaler, and feature names
model = joblib.load("intrusion_detection_model.pkl")
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")


# Prediction function
def predict_intrusion(data):
    df = pd.DataFrame([data])
    for col in feature_names:
        if col not in df:
            df[col] = 0
    df = df[feature_names]
    df_scaled = scaler.transform(df)
    prediction = model.predict(df_scaled)
    return "🔵 Normal Connection" if prediction[0] == 0 else "🔴 Intrusion Detected (Attack!)"


# Ensure session state has a page tracker
if "page" not in st.session_state:
    st.session_state.page = 1

# Navigation buttons
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# Page 1: Introduction and Description
if st.session_state.page == 1:
    st.title("🔍 Intrusion Detection System")
    st.subheader("Protect Your Network from Unauthorized Access 🚀")
    st.write(
        """
Welcome to the **Intrusion Detection System (IDS)**!  
This app uses **Machine Learning** to detect whether a network connection is **normal** or **malicious**.  

### 🚀 Features:
- **Real-time prediction** of network traffic  
- **Detects common attack patterns**  
- **User-friendly input interface**  

Click **Next** to start entering your network details and predict possible intrusions! 🔥
        """
    )

    # "Next" button for navigation
    if st.button("➡️ Next"):
        next_page()

# Page 2: Input Features and Prediction
elif st.session_state.page == 2:
    st.title("🔧 Enter Network Details")
    st.write("Fill in the following details to predict potential intrusions:")

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
