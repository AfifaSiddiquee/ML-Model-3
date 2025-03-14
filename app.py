# Import necessary libraries
import streamlit as st
import pickle

# Load the trained model
model = pickle.load(open("intrusion_detection_model.pkl", "rb"))

# Set Streamlit page configuration
st.set_page_config(page_title="Intrusion Detection System", layout="wide")

# Custom CSS for styling and centering content
st.markdown(
    """
    <style>
    /* Center the main content */
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
    }

    /* Style for the content box */
    .content-box {
        text-align: center;
        max-width: 600px;
        padding: 20px;
    }

    /* Header styling */
    h1 {
        font-size: 3rem;
        font-weight: bold;
        color: #4A90E2;
    }

    h2 {
        font-size: 1.5rem;
        color: #555;
    }

    /* Button styling */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.8rem 1.5rem;
        font-size: 1.2rem;
        border-radius: 10px;
        transition: 0.3s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centering the content
st.markdown('<div class="main"><div class="content-box">', unsafe_allow_html=True)

# Title and Subtitle
st.title("🔍 Intrusion Detection System")
st.subheader("Protect Your Network from Unauthorized Access 🚀")

# App introduction
st.write(
    """
Welcome to the **Intrusion Detection System (IDS)**!  
This app uses **Machine Learning** to detect whether a network connection is **normal** or **malicious**.
"""
)

# Features section
st.markdown("### 🚀 Features:")
st.markdown("- **Real-time prediction** of network traffic")
st.markdown("- **Detects common attack patterns**")
st.markdown("- **User-friendly input interface**")

# Navigation button to move forward
if st.button("Next ➡️"):
    st.write("Let's move to the next step!")

# Close the content div
st.markdown("</div></div>", unsafe_allow_html=True)

# Placeholder for future network details input
st.markdown("## 🛠️ Enter Network Details")
st.write("Fill in the details below to predict potential intrusions:")

# Example of user inputs
ip_address = st.text_input("Enter IP Address")
port = st.number_input("Enter Port Number", min_value=0, max_value=65535)
protocol = st.selectbox("Select Protocol", ["TCP", "UDP", "ICMP"])

# Predict button
if st.button("Predict 🚨"):
    # Example prediction (dummy prediction for now)
    prediction = model.predict([[port]])  # Assuming model takes port as input

    if prediction[0] == 1:
        st.error("⚠️ **Potential Intrusion Detected!**")
    else:
        st.success("✅ **Connection looks safe!**")

