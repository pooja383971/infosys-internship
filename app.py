import streamlit as st
import requests
import json

st.title("Contract AI Analyzer")
st.markdown("Upload a PDF contract to analyze it using AI-powered pipeline.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    if st.button("Analyze Contract"):
        with st.spinner("Analyzing contract... This may take a few moments."):
            try:
                # Send file to FastAPI server
                files = {"file": uploaded_file}
                response = requests.post("http://localhost:8000/analyze", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis complete!")
                    
                    # Display results
                    st.header("Analysis Results")
                    
                    st.subheader("Domain Classification")
                    st.write(f"**Domain:** {result.get('domain', 'N/A')}")
                    
                    st.subheader("Agents Used")
                    agents = result.get('agents', [])
                    st.write(", ".join(agents) if agents else "No agents used")
                    
                    st.subheader("Agent Results")
                    agent_results = result.get('results', {})
                    if agent_results:
                        for agent, res in agent_results.items():
                            st.write(f"**{agent}:** {res}")
                    else:
                        st.write("No agent results available")
                    
                    st.subheader("PDF Report")
                    pdf_path = result.get('pdf_report')
                    if pdf_path:
                        st.write(f"Report generated: {pdf_path}")
                    else:
                        st.write("No PDF report generated")
                    
                    # Show raw JSON if needed
                    with st.expander("Raw JSON Response"):
                        st.json(result)
                        
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
                st.info("Make sure the FastAPI server is running on http://localhost:8000")
                
else:
    st.info("Please upload a PDF file to begin analysis.")

st.markdown("---")
st.markdown("**Note:** Ensure the backend API server is running before analyzing contracts.")