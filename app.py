import streamlit as st
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DDI Clinical Checker",
    page_icon="💊",
    layout="centered"
)

# ---------------- SESSION STATE (Consent Logic) ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False

# ================= 1. ENTRY CONSENT SCREEN =================
if not st.session_state.accepted:
    st.markdown("""
    <div style="padding:30px; border-radius:16px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); line-height:1.6;">
        <h2>💊 DDI Clinical Checker</h2>
        <h4>Drug-Drug Interaction Screening Interface</h4>
        <hr>
        [span_6](start_span)<b>Purpose:</b> This prototype identifies potential clinical risks when taking multiple medications simultaneously[span_6](end_span).
        <br><br>
        [span_7](start_span)<b>⚠ Important Notice:</b> This software is a <b>B.Pharm clinical decision-support prototype</b> for educational purposes only[span_7](end_span). 
        [span_8](start_span)[span_9](start_span)It does not replace a doctor's consultation or laboratory diagnosis[span_8](end_span)[span_9](end_span).
    </div>
    """, unsafe_allow_html=True)

    agree = st.checkbox("I understand this system provides screening support only.")
    if agree and st.button("Enter Clinical Screening Interface"):
        st.session_state.accepted = True
        st.rerun()
    st.stop()

# ================= 2. HEADER & DATA LOADING =================
st.title("💊 DDI Clinical Checker")
[span_10](start_span)st.caption("Community Pharmacy Interaction Assistant | Risk Classification | Clinical Guidance[span_10](end_span)")

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return []

interactions = load_data()
all_drugs = sorted(list(set([i['drug1'] for i in interactions] + [i['drug2'] for i in interactions])))

# ================= 3. INPUT PANEL =================
st.subheader("👤 Medication Profile")
col1, col2 = st.columns(2)

with col1:
    drug_a = st.selectbox("Select First Medication", options=all_drugs, index=None, placeholder="Search...")

with col2:
    drug_b = st.selectbox("Select Second Medication", options=all_drugs, index=None, placeholder="Search...")

dosage_freq = st.select_slider(
    "Combined Dosage Frequency (Total doses per day)",
    options=["1 time", "2 times", "3 times", "4+ times"]
)

st.divider()

# ================= 4. INTERACTION ENGINE =================
def assess_ddi(d1, d2):
    res = next((item for item in interactions if 
                (item['drug1'] == d1 and item['drug2'] == d2) or 
                (item['drug1'] == d2 and item['drug2'] == d1)), None)
    return res

# ================= 5. RESULTS INTERFACE =================
[span_11](start_span)if st.button("Run Clinical Screening[span_11](end_span)"):
    if not drug_a or not drug_b:
        st.warning("Please select both medications.")
    elif drug_a == drug_b:
        st.info("Same medication selected. No interaction found.")
    else:
        result = assess_ddi(drug_a, drug_b)
        
        st.subheader("🧠 Clinical Impression")
        if result:
            # [span_12](start_span)Color-coded Risk Level[span_12](end_span)
            if result['level'] == "RED":
                st.error(f"HIGH RISK INTERACTION: {result['level']}")
                st.subheader("🚨 Clinical Alert")
                st.write(result['message'])
                [span_13](start_span)st.error("Immediate pharmacist or physician consultation required[span_13](end_span).")
            else:
                st.warning(f"MODERATE RISK INTERACTION: {result['level']}")
                st.subheader("📖 Clinical Explanation")
                st.write(result['message'])
        else:
            st.success("✅ NO MAJOR INTERACTION DETECTED")
            st.write(f"No significant documented interactions between **{drug_a}** and **{drug_b}** in our current clinical database.")

st.divider()
[span_14](start_span)st.caption("DDI Clinical Checker | B.Pharm Final Year Project Prototype[span_14](end_span)")
