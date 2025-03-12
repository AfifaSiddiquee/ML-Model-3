import streamlit as st
import pandas as pd
import joblib

# Load trained model, scaler, and feature names
model = joblib.load("intrusion_detection_model.pkl")
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")  # Load saved feature names

# Define function for prediction
def predict_intrusion(data):
    df = pd.DataFrame([data])
    for col in feature_names:
        if col not in df:
            df[col] = 0
    df = df[feature_names]
    df_scaled = scaler.transform(df)
    prediction = model.predict(df_scaled)
    return "🔵 Normal Connection" if prediction[0] == 0 else "🔴 Intrusion Detected (Attack!)"

# Sidebar details
st.sidebar.title("📖 About the IDS App")
st.sidebar.write("""
🔹 **Machine Learning-based Intrusion Detection System (IDS)**
🔹 Identifies **malicious network traffic** to **protect networks**
🔹 **How to use:**
&nbsp;&nbsp;&nbsp; 1️⃣ Enter network details below
&nbsp;&nbsp;&nbsp; 2️⃣ Click **"Detect Intrusion"**
&nbsp;&nbsp;&nbsp; 3️⃣ Get a prediction: **Normal 🔵** or **Intrusion 🔴**
""")

# Custom CSS to reduce spacing
st.markdown(
    """
    <style>
    .compact-text {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 3px;
    }
    .description {
        font-size: 14px;
        color: gray;
        margin-bottom: 0px;
    }
    .stNumberInput, .stSelectbox {
        margin-top: 0px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title
st.title("🔍 Intrusion Detection System")
st.subheader("Protect Your Network from Unauthorized Access")

# Grouped layout for inputs
fields = [
    ("Count", "Number of connections to the same host in a short time.", st.number_input, {"min_value": 0, "value": 5, "key": "count"}),
    ("Source Bytes", "Data sent from source to destination (in bytes).", st.number_input, {"min_value": 0, "value": 500, "key": "src_bytes"}),
    ("Logged In", "Indicates whether the user is logged in (1 = Yes, 0 = No).", st.selectbox, {"options": [0, 1], "key": "logged_in"}),
    ("Service Error Rate", "Percentage of connections that have SYN errors.", st.number_input, {"min_value": 0.0, "max_value": 1.0, "value": 0.2, "key": "srv_serror_rate"}),
    ("Destination Bytes", "Data sent from destination to source (in bytes).", st.number_input, {"min_value": 0, "value": 1000, "key": "dst_bytes"}),
    ("Service Count", "Number of connections to the same service.", st.number_input, {"min_value": 0, "value": 10, "key": "srv_count"})
]

# Render inputs in a compact two-column layout
for feature, description, input_type, kwargs in fields:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<p class='compact-text'>{feature}:</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p class='description'>{description}</p>", unsafe_allow_html=True)
        input_type("", **kwargs)

# Predict button
if st.button("🔍 Detect Intrusion"):
    input_data = {field[0].lower().replace(" ", "_"): st.session_state[field[3]["key"]] for field in fields}
    result = predict_intrusion(input_data)
    st.success(f"**Prediction: {result}**")
