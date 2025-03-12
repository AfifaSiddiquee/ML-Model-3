import streamlit as st

# Define styling for feature names
feature_style = "<p style='font-size:16px; font-weight:bold; margin-bottom:5px;'>"

st.title("🔍 Intrusion Detection System")
st.subheader("Protect Your Network from Unauthorized Access")

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
