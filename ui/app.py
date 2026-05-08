# import streamlit as st
# import requests
# import tempfile

# # FASTAPI_URL = "http://127.0.0.1:8000/analyze"
# FASTAPI_URL = "http://127.0.0.1:8000/analyze"


# st.set_page_config(page_title="Contract AI Analyzer", layout="wide")

# st.title("📄 Contract AI Analyzer")
# st.subheader("Upload Contract PDF")

# uploaded_file = st.file_uploader("Drag and drop a PDF here", type=["pdf"])

# if uploaded_file is not None:
#     if st.button("Analyze Contract"):
#         with st.spinner("Analyzing... please wait ⏳"):
#             temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#             temp.write(uploaded_file.read())
#             temp.close()

#             with open(temp.name, "rb") as f:
#                 files = {"file": (uploaded_file.name, f, "application/pdf")}
#                 response = requests.post(FASTAPI_URL, files=files)

#             if response.status_code == 200:
#                 data = response.json()

#                 st.success("✅ Analysis Complete!")
#                 st.subheader("🔍 Domain Detected:")
#                 st.write(data["domain"])

#                 st.subheader("🧠 Agents Used:")
#                 st.write(", ".join(data["agents"]))

#                 st.subheader("📑 Extracted Contract Text (preview):")
#                 st.text_area("", data["contract_text"][:1000] + "...")

#                 st.subheader("📌 Agent Findings:")
#                 for agent, result in data["results"].items():
#                     st.write(f"### 🤖 {agent}")
#                     st.code(result)

#                 st.subheader("📥 Report:")
#                 st.write(f"Generated PDF: {data['pdf_report']}")

#             else:
#                 st.error("❌ API Error: " + response.text)

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from PyPDF2 import PdfReader

app = FastAPI(title="Contract AI Backend")

# Allow Streamlit access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# PDF Text Extraction
# -----------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text.strip()

# -----------------------------
# Simple Domain Detection
# -----------------------------
def detect_domain(text: str) -> str:
    text = text.lower()
    if "agreement" in text or "party" in text:
        return "Legal"
    elif "payment" in text or "invoice" in text:
        return "Finance"
    elif "policy" in text or "compliance" in text:
        return "Compliance"
    else:
        return "General"

# -----------------------------
# MAIN ENDPOINT
# -----------------------------
@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    # Extract text
    contract_text = extract_text_from_pdf(temp_path)

    # Detect domain
    domain = detect_domain(contract_text)

    # Agent simulation
    agents = ["LegalAgent", "ComplianceAgent", "FinanceAgent"]

    results = {
        "LegalAgent": "Reviewed clauses, responsibilities, and termination terms.",
        "ComplianceAgent": "Checked regulatory and policy compliance.",
        "FinanceAgent": "Analyzed payment terms and financial risks."
    }

    pdf_report = "contract_analysis_report.pdf"

    # Cleanup
    os.remove(temp_path)

    return {
        "domain": domain,
        "agents": agents,
        "contract_text": contract_text,
        "results": results,
        "pdf_report": pdf_report
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {"status": "FastAPI backend running"}
