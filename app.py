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


# Sidebar content
st.sidebar.title("📖 About the IDS App")
st.sidebar.write(
    """
🔹 **Machine Learning-based Intrusion Detection System (IDS)**  
🔹 Identifies **malicious network traffic** to **protect networks**  
🔹 **How to use:**  
1️⃣ Enter network details below  
2️⃣ Click **"Detect Intrusion"**  
3️⃣ Get a prediction: **Normal 🔵** or **Intrusion 🔴**
"""
)

# Improved CSS to reduce spacing and tighten layout
st.markdown(
    """
    <style>
    /* Adjust spacing around main content */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Reduce space between labels and inputs */
    .stMarkdown p {
        margin-bottom: -5px !important;
        font-size: 14px;
    }

    /* Adjust input margins to pull closer */
    .stNumberInput, .stSelectbox {
        margin-top: -10px !important;
        margin-bottom: 5px !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        font-size: 16px;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main App Title
st.title("🔍 Intrusion Detection System")
st.subheader("Protect Your Network from Unauthorized Access 🚀")

# Input fields
fields = [
    ("Count", "Number of connections to the same host in a short time.", st.number_input, {"min_value": 0, "value": 5, "key": "count"}),
    ("Source Bytes", "Data sent from source to destination (in bytes).", st.number_input, {"min_value": 0, "value": 500, "key": "src_bytes"}),
    ("Logged In", "User logged in? (1 = Yes, 0 = No)", st.selectbox, {"options": [0, 1], "key": "logged_in"}),
    ("Service Error Rate", "Percentage of connections with errors.", st.number_input, {"min_value": 0.0, "max_value": 1.0, "value": 0.2, "key": "srv_serror_rate"}),
    ("Destination Bytes", "Data sent from destination to source.", st.number_input, {"min_value": 0, "value": 1000, "key": "dst_bytes"}),
    ("Service Count", "Number of connections to the same service.", st.number_input, {"min_value": 0, "value": 10, "key": "srv_count"}),
]

# Display inputs with tight layout
for feature, description, input_type, kwargs in fields:
    st.markdown(f"**{feature}:**")
    st.markdown(f"<p style='font-size:12px; color:#555; margin-top:-8px; margin-bottom:-5px;'>{description}</p>", unsafe_allow_html=True)
    input_type("", **kwargs)

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
