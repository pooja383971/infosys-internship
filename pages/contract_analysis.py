import streamlit as st

st.title("📄 Contract Analysis System")
st.write("Upload a contract to analyze clauses, risks, and summaries.")

uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])

if uploaded_file:
    st.success("Contract uploaded successfully!")
