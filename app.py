import streamlit as st
import re
import os
from datetime import date
import google.generativeai as genai
from dotenv import load_dotenv
from database import init_db, create_patient, read_all_patients, update_patient, delete_patient

# Load API key and init database
load_dotenv(override=True)
init_db()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Missing Gemini API Key. Please check your .env file.")

def call_gemini(glucose, haemoglobin, cholesterol):
    if not API_KEY:
        return "AI Prediction Offline (Missing API Key)."
    try:
        prompt = f"""
        Analyze these blood test results for a patient screening:
        - Fasting Glucose: {glucose} mg/dL
        - Haemoglobin: {haemoglobin} g/dL
        - Total Cholesterol: {cholesterol} mg/dL

        Give a concise 1-2 sentence health screening summary indicating 
        possible risk levels (normal, diabetic risk, anemia, or cardiac risk).
        Be professional and direct. Under 30 words. No bullet points.
        """
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"API Error: {str(e)}"

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

# Page config
st.set_page_config(page_title="MIRA Health Intelligence", layout="wide")
st.title("🏥 MIRA — Medical Intelligence Robotic Automation")
st.markdown("*Patient Diagnostic Portal*")
st.markdown("---")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("➕ Add New Patient")
    with st.form("add_patient_form", clear_on_submit=True):
        full_name    = st.text_input("Full Name")
        dob          = st.date_input("Date of Birth", max_value=date.today())
        email        = st.text_input("Email Address")

        st.markdown("**Blood Test Values**")
        glucose      = st.number_input("Glucose (mg/dL)",      min_value=0.0, step=1.0)
        haemoglobin  = st.number_input("Haemoglobin (g/dL)",   min_value=0.0, step=0.1)
        cholesterol  = st.number_input("Cholesterol (mg/dL)",  min_value=0.0, step=1.0)

        submit = st.form_submit_button("🔬 Generate AI Remarks & Save")

        if submit:
            if not full_name or not email:
                st.error("Name and Email cannot be empty.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif dob > date.today():
                st.error("Date of birth cannot be a future date.")
            elif glucose == 0 or haemoglobin == 0 or cholesterol == 0:
                st.error("Blood test values must be greater than 0.")
            else:
                with st.spinner("Analyzing with MIRA AI Engine..."):
                    remarks = call_gemini(glucose, haemoglobin, cholesterol)
                    create_patient(full_name, str(dob), email,
                                   glucose, haemoglobin, cholesterol, remarks)
                    st.success("✅ Patient record saved successfully!")
                    st.rerun()

with col2:
    st.subheader("📋 Patient Records")
    records = read_all_patients()

    if not records:
        st.info("No patient records found. Add one using the form.")
    else:
        for record in records:
            p_id, name, p_dob, p_email, glu, hgb, chol, rem = record

            with st.expander(f"🧑‍⚕️ #{p_id} — {name}"):
                e_name  = st.text_input("Full Name",  value=name,    key=f"n_{p_id}")
                e_dob   = st.text_input("DOB (YYYY-MM-DD)", value=p_dob, key=f"d_{p_id}")
                e_email = st.text_input("Email",      value=p_email, key=f"e_{p_id}")

                c1, c2, c3 = st.columns(3)
                with c1:
                    e_glu  = st.number_input("Glucose",      value=glu,  key=f"g_{p_id}")
                with c2:
                    e_hgb  = st.number_input("Haemoglobin",  value=hgb,  key=f"h_{p_id}")
                with c3:
                    e_chol = st.number_input("Cholesterol",  value=chol, key=f"c_{p_id}")

                st.info(f"**AI Remarks:** {rem}")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("💾 Update Record", key=f"up_{p_id}"):
                        with st.spinner("Re-analyzing..."):
                            new_rem = call_gemini(e_glu, e_hgb, e_chol)
                            update_patient(p_id, e_name, e_dob, e_email,
                                           e_glu, e_hgb, e_chol, new_rem)
                            st.success("Record updated!")
                            st.rerun()
                with b2:
                    if st.button("🗑️ Delete Record", key=f"del_{p_id}"):
                        delete_patient(p_id)
                        st.warning("Record deleted.")
                        st.rerun()