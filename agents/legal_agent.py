from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

HF_API_KEY = os.getenv("HF_API_KEY")  # Get token from env
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"

client = InferenceClient(model=MODEL_ID, token=HF_API_KEY)

def legal_agent(contract_text: str) -> str:
    prompt = f"""
    You are a Legal Expert.
    Task: Identify legal risks in the contract.
    Output format (JSON lines):
    {{
      "clause": "...",
      "risk": "...",
      "severity": "Low/Medium/High"
    }}

    CONTRACT:
    {contract_text}
    """

    messages = [{"role": "user", "content": prompt}]
    response = client.chat_completion(messages, max_tokens=800, temperature=0.3)

    return response.choices[0].message["content"].strip()
