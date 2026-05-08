# import streamlit as st
# import requests
# import json

# st.title("Contract AI Analyzer")
# st.markdown("Upload a PDF contract to analyze it using AI-powered pipeline.")

# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# if uploaded_file is not None:
#     st.success("File uploaded successfully!")
    
#     if st.button("Analyze Contract"):
#         with st.spinner("Analyzing contract... This may take a few moments."):
#             try:
#                 # Send file to FastAPI server
#                 files = {"file": uploaded_file}
#                 response = requests.post("http://localhost:8000/analyze", files=files)
                
#                 if response.status_code == 200:
#                     result = response.json()
                    
#                     st.success("Analysis complete!")
                    
#                     # Display results
#                     st.header("Analysis Results")
                    
#                     st.subheader("Domain Classification")
#                     st.write(f"**Domain:** {result.get('domain', 'N/A')}")
                    
#                     st.subheader("Agents Used")
#                     agents = result.get('agents', [])
#                     st.write(", ".join(agents) if agents else "No agents used")
                    
#                     st.subheader("Agent Results")
#                     agent_results = result.get('results', {})
#                     if agent_results:
#                         for agent, res in agent_results.items():
#                             st.write(f"**{agent}:** {res}")
#                     else:
#                         st.write("No agent results available")
                    
#                     st.subheader("PDF Report")
#                     pdf_path = result.get('pdf_report')
#                     if pdf_path:
#                         st.write(f"Report generated: {pdf_path}")
#                     else:
#                         st.write("No PDF report generated")
                    
#                     # Show raw JSON if needed
#                     with st.expander("Raw JSON Response"):
#                         st.json(result)
                        
#                 else:
#                     st.error(f"Error: {response.status_code} - {response.text}")
                    
#             except requests.exceptions.RequestException as e:
#                 st.error(f"Connection error: {e}")
#                 st.info("Make sure the FastAPI server is running on http://localhost:8000")
                
# else:
#     st.info("Please upload a PDF file to begin analysis.")

# st.markdown("---")
# st.markdown("**Note:** Ensure the backend API server is running before analyzing contracts.")
import streamlit as st
import requests
import base64
import os

# ---------------- CONFIG ----------------
FASTAPI_URL = "http://127.0.0.1:8000/analyze"
REQUEST_TIMEOUT = 120
# ---------------------------------------

st.set_page_config(
    page_title="Contract AI Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📑 Contract AI Analyzer")
st.markdown("Upload a **PDF contract** to analyze it using an AI-powered pipeline.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")

    if st.button("🚀 Analyze Contract"):
        with st.spinner("Analyzing contract... Please wait."):

            try:
                # Correct PDF upload format
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    FASTAPI_URL,
                    files=files,
                    timeout=REQUEST_TIMEOUT
                )

                if response.status_code != 200:
                    st.error(f"❌ API Error {response.status_code}")
                    st.code(response.text)
                    st.stop()

                result = response.json()
                st.success("🎉 Analysis completed!")

                # ---------------- RESULTS ----------------
                st.header("📊 Analysis Results")

                st.subheader("📌 Domain Classification")
                st.write(result.get("domain", "N/A"))

                st.subheader("🤖 Agents Used")
                agents = result.get("agents", [])
                st.write(", ".join(agents) if agents else "No agents used")

                st.subheader("🧠 Agent Outputs")
                agent_results = result.get("results", {})
                if agent_results:
                    for agent, output in agent_results.items():
                        st.markdown(f"**{agent}:**")
                        st.write(output)
                else:
                    st.write("No agent outputs available")

                # ---------------- PDF DOWNLOAD ----------------
                st.subheader("📥 Download Report")

                # OPTION 1: Base64 PDF (BEST)
                pdf_base64 = result.get("pdf_base64")
                if pdf_base64:
                    pdf_bytes = base64.b64decode(pdf_base64)

                    st.download_button(
                        label="⬇️ Download Analysis PDF",
                        data=pdf_bytes,
                        file_name="contract_analysis_report.pdf",
                        mime="application/pdf"
                    )

                # OPTION 2: Local file path (fallback)
                else:
                    pdf_path = result.get("pdf_report")
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Analysis PDF",
                                data=f,
                                file_name="contract_analysis_report.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.warning("⚠️ PDF report not available.")

                # ---------------- RAW JSON ----------------
                with st.expander("🧾 Raw API Response"):
                    st.json(result)

            except requests.exceptions.ConnectionError:
                st.error("❌ Backend server not running")
                st.info("Start FastAPI using:\n\n`uvicorn api.main:app --reload --port 8000`")

            except requests.exceptions.Timeout:
                st.error("⏳ Request timed out. Try again.")

            except Exception as e:
                st.error("Unexpected error occurred")
                st.exception(e)

else:
    st.info("📄 Please upload a PDF file to begin.")

st.markdown("---")
st.caption("⚠️ Ensure FastAPI backend is running before analysis.")
