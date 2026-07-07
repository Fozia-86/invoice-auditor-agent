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

# Excel Database file ka naam fix karein
DB_FILE = "audit_database.csv"

# =====================================================================
# 🛠️ 1. MOCK EMAIL FUNCTION
# =====================================================================
def send_email_alert(vendor, invoice_num, total, status, report_text):
    """Local simulation mode to instantly bypass Google/SendGrid restrictions"""
    manager_email = os.getenv("MANAGER_EMAIL", "manager@company.com")
    
    # Streamlit UI par visual banner
    st.error(f"📧 [SYSTEM ALERT] Automated Forensic Notification Sent to Manager ({manager_email})!")
    
    # Terminal runtime log debug karne ke liye
    print("\n" + "📧 " + "="*20 + " AUTOMATED EMAIL SIMULATION " + "="*20)
    print(f"To: {manager_email}")
    print(f"Subject: ⚠️ EXCEPTION FLAG DETECTED - Vendor: {vendor}")
    print(f"Body: Invoice #{invoice_num} for amount {total} has triggered system warnings with status '{status}'.")
    print("="*60 + "\n")

# --- Database Function ---
def save_to_database(vendor, invoice_num, total, status):
    """Extracted data ko Excel/CSV file mein save karne ke liye"""
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

# --- AI Auditor Function ---
def audit_invoice_ai(file_bytes, file_type):
    """Gemini API ko call karne aur audit report nikalne ka function"""
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

# --- Streamlit Web UI Dashboard ---
st.set_page_config(page_title="AI Batch Invoice Auditor", layout="wide")

st.title("📋 AI Batch Invoice Auditor Dashboard")
st.write("Upload multiple invoice images or PDFs to audit them simultaneously and log data into the Excel Database.")

# Do Columns banayein
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔍 Audit Invoices (Batch Mode)")
    
    uploaded_files = st.file_uploader(
        "Choose Invoice Files", 
        type=["jpg", "jpeg", "png", "pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} files selected.")
        
        if st.button("🚀 Run Batch AI Audit"):
            for index, uploaded_file in enumerate(uploaded_files):
                st.subheader(f"📄 Processing File {index+1}: {uploaded_file.name}")
                
                with st.spinner(f"Analyzing {uploaded_file.name} with Gemini AI..."):
                    try:
                        file_bytes = uploaded_file.read()
                        file_type = uploaded_file.type
                        
                        raw_result = audit_invoice_ai(file_bytes, file_type)
                        
                        vendor = "Unknown"
                        inv_num = "Unknown"
                        total = "0"
                        status = "Review Required"
                        
                        if "---DATA_START---" in raw_result:
                            data_part = raw_result.split("---DATA_START---")[1].split("---DATA_END---")[0]
                            for line in data_part.strip().split("\n"):
                                if line.startswith("Vendor:"): vendor = line.replace("Vendor:", "").strip()
                                if line.startswith("InvoiceNumber:"): inv_num = line.replace("InvoiceNumber:", "").strip()
                                if line.startswith("TotalAmount:"): total = line.replace("TotalAmount:", "").strip()
                                if line.startswith("Status:"): status = line.replace("Status:", "").strip()
                        
                        clean_report = raw_result.split("---DATA_END---")[-1]
                        
                        # Save to CSV Database
                        save_to_database(vendor, inv_num, total, status)
                        
                        # =====================================================================
                        # 📩 2. EMAIL CONDITION TRIGGER
                        # =====================================================================
                        if status.lower() in ["flagged", "rejected"]:
                            send_email_alert(vendor, inv_num, total, status, clean_report)
                        
                        with st.expander(f"✅ View Audit Report for {uploaded_file.name}", expanded=True):
                            st.markdown(clean_report)
                            
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
            st.success("🎉 All selected invoices have been processed and logged!")
            st.rerun()

with col2:
    st.header("📊 Audited Records Database")
    if os.path.exists(DB_FILE):
        df_db = pd.read_csv(DB_FILE)
        st.dataframe(df_db.iloc[::-1], use_container_width=True)
        
        csv_data = df_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Database as CSV",
            data=csv_data,
            file_name="Invoice_Audit_Logs.csv",
            mime="text/csv"
        )
    else:
        st.info("No records found in the database yet. Run a batch audit to log entries.")