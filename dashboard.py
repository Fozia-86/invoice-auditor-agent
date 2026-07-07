import os
import datetime
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

# Gemini Client initialize karein
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DB_FILE = "audit_database.csv"

def send_email_alert(vendor, invoice_num, total, status, report_text):
    manager_email = os.getenv("MANAGER_EMAIL", "manager@company.com")
    st.error(f"📧 [SYSTEM ALERT] Automated Forensic Notification Sent to Manager ({manager_email})!")

def save_to_database(vendor, invoice_num, total, status):
    new_data = {
        "Timestamp": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Vendor Name": [vendor],
        "Invoice Number": [invoice_num],
        "Total Amount": [total],
        "Audit Status": [status]
    }
    df_new = pd.DataFrame(new_data)
    if os.path.exists(DB_FILE):
        df_old = pd.read_csv(DB_FILE)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new
    df_final.to_csv(DB_FILE, index=False)

def audit_invoice_ai(file_bytes, file_type):
    invoice_part = types.Part.from_bytes(data=file_bytes, mime_type=file_type)
    audit_prompt = """
    You are an expert Invoice Auditor. Analyze this invoice carefully.
    Provide the response in two clear sections:
    ---DATA_START---
    Vendor: [Only Vendor Name]
    InvoiceNumber: [Only Invoice/Lab Number]
    TotalAmount: [Only Numeric Value, e.g. 2200]
    Status: [Approved / Rejected / Flagged]
    ---DATA_END---
    ## 📋 Invoice Audit Summary
    Provide the visual markdown report here with Findings, Flagged Issues, and Final Recommendation.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[invoice_part, audit_prompt]
    )
    return response.text

# --- Streamlit Web UI ---
st.set_page_config(page_title="AI Batch Invoice Auditor", layout="wide")
st.title("📋 AI Batch Invoice Auditor Dashboard")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔍 Audit Invoices (Batch Mode)")
    uploaded_files = st.file_uploader("Choose Invoice Files", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 Run Batch AI Audit"):
            for index, uploaded_file in enumerate(uploaded_files):
                with st.spinner(f"Analyzing {uploaded_file.name}..."):
                    try:
                        file_bytes = uploaded_file.read()
                        file_type = uploaded_file.type
                        raw_result = audit_invoice_ai(file_bytes, file_type)
                        
                        vendor, inv_num, total, status = "Unknown", "Unknown", "0", "Review Required"
                        if "---DATA_START---" in raw_result:
                            data_part = raw_result.split("---DATA_START---")[1].split("---DATA_END---")[0]
                            for line in data_part.strip().split("\n"):
                                if line.startswith("Vendor:"): vendor = line.replace("Vendor:", "").strip()
                                if line.startswith("InvoiceNumber:"): inv_num = line.replace("InvoiceNumber:", "").strip()
                                if line.startswith("TotalAmount:"): total = line.replace("TotalAmount:", "").strip()
                                if line.startswith("Status:"): status = line.replace("Status:", "").strip()
                        
                        clean_report = raw_result.split("---DATA_END---")[-1]
                        save_to_database(vendor, inv_num, total, status)
                        
                        if status.lower() in ["flagged", "rejected"]:
                            send_email_alert(vendor, inv_num, total, status, clean_report)
                        
                        with st.expander(f"✅ Report: {uploaded_file.name}", expanded=True):
                            st.markdown(clean_report)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            st.success("🎉 Processed!")
            st.rerun()

with col2:
    st.header("📊 Audited Records Database")
    if os.path.exists(DB_FILE):
        df_db = pd.read_csv(DB_FILE)
        st.dataframe(df_db.iloc[::-1], use_container_width=True)
    else:
        st.info("No records found yet.")