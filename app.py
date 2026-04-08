import streamlit as st
import json

# ---------------- 1. PAGE CONFIG ----------------
st.set_page_config(
    page_title="DDI Clinical Checker",
    page_icon="💊",
    layout="centered"
)

# ---------------- 2. SESSION STATE (Consent Logic) ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False

# ================= 3. ENTRY CONSENT SCREEN =================
if not st.session_state.accepted:
    st.markdown("""
    <div style="padding:30px; border-radius:16px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); line-height:1.6;">
        <h2>🩺 DDI Clinical Checker</h2>
        <h4>Clinical Decision Support Screening Interface</h4>
        <hr>
        <b>Purpose of this system:</b><br>
        This application is designed as a <b>community-pharmacy clinical screening assistant</b> 
        [span_3](start_span)that helps identify potential drug-drug interaction risks before dispensing medications[span_3](end_span).
        <br><br>
        <b>⚠ Important Notice:</b><br>
        This software is developed as a <b>B.Pharm clinical decision-support prototype</b> 
        [span_4](start_span)for educational and screening purposes only[span_4](end_span). Users are strongly advised to consult 
        [span_5](start_span)a qualified healthcare professional for accurate diagnosis and treatment[span_5](end_span).
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    agree = st.checkbox("I understand this system provides screening support only and does not replace professional medical consultation.")

    if agree:
        if st.button("Enter Clinical Screening Interface"):
            st.session_state.accepted = True
            st.rerun()
    st.stop()

# ================= 4. HEADER =================
st.title("🩺 DDI Clinical Checker")
st.caption("Community Pharmacy Interaction Assistant | Risk Classification | Clinical Guidance")
st.divider()

# ================= 5. DATA LOADING =================
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        st.error("Database (data.json) not found or formatted incorrectly.")
        return []

interactions = load_data()

# Extract unique drugs for the dropdowns
all_drugs = set()
for item in interactions:
    all_drugs.add(item.get('drug1'))
    all_drugs.add(item.get('drug2'))
drug_options = sorted([d for d in all_drugs if d])

# ================= 6. INPUT PANEL =================
st.subheader("👤 Medication Profile")
col1, col2 = st.columns(2)

with col1:
    drug_a = st.selectbox("Select First Medication", options=drug_options, index=None, placeholder="Type to search...")

with col2:
    drug_b = st.selectbox("Select Second Medication", options=all_drugs, index=None, placeholder="Type to search...")

[span_6](start_span)severity = st.slider("Patient Sensitivity / Severity Level", 1, 10, 3) # Modeled after friend's severity slider[span_6](end_span)
st.divider()

# ================= 7. SCREENING LOGIC =================
if st.button("Run Clinical Screening"):
    if not drug_a or not drug_b:
        st.warning("Please select both medications.")
    elif drug_a == drug_b:
        st.info("Same medication selected. No interaction found.")
    else:
        # Search for interaction in both directions
        res = next((item for item in interactions if 
                    (item['drug1'] == drug_a and item['drug2'] == drug_b) or 
                    (item['drug1'] == drug_b and item['drug2'] == drug_a)), None)

        st.subheader("🧠 Clinical Impression")
        
        if res:
            if res['level'] == "RED":
                st.error(f"HIGH RISK: {res['level']}")
                st.subheader("🚨 Red Flag Indicators")
                st.write(f"• {res['message']}")
                st.error("Immediate pharmacist intervention or physician referral required.")
            else:
                st.warning(f"MODERATE RISK: {res['level']}")
                st.subheader("📖 Clinical Explanation")
                st.write(res['message'])
        else:
            st.success("✅ No Major Interaction Detected")
            st.write("No significant documented interactions found in the current database for this combination.")

st.divider()
st.caption("DDI Clinical Checker | Clinical Decision Support Prototype | B.Pharm Project")
