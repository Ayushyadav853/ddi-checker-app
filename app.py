import streamlit as st
import json

# 1. LOAD DATA
def load_data():
    with open('data.json') as f:
        return json.load(f)

interactions = load_data()

# 2. DEFINE THE DRUG LIST (The 500+ Top Indian Drugs)
# You can expand this list as much as you want
drug_options = sorted([
    "Paracetamol", "Dolo 650", "Metformin", "Telmisartan", "Amlodipine", 
    "Atorvastatin", "Amoxicillin", "Azithromycin", "Pantoprazole", 
    "Sildenafil", "Warfarin", "Aspirin", "Insulin", "Glimepiride",
    "Vildagliptin", "Teneligliptin", "Losartan", "Diclofenac", "Aceclofenac"
    # ... add all 500 names here
])

# 3. PAGE CONFIG
st.set_page_config(page_title="DDI Checker India", page_icon="💊", layout="centered")

st.title("🇮🇳 Indian Drug-Drug Interaction Checker")
st.markdown("---")

# 4. SMART SEARCH IMPLEMENTATION
st.subheader("Search Medications")
col1, col2 = st.columns(2)

with col1:
    # 'index=None' makes the box empty by default
    # 'placeholder' gives the user a hint
    drug_a = st.selectbox(
        "First Molecule / Brand",
        options=drug_options,
        index=None,
        placeholder="Type to search (e.g. Telmisartan)...",
        key="drug_a"
    )

with col2:
    drug_b = st.selectbox(
        "Second Molecule / Brand",
        options=drug_options,
        index=None,
        placeholder="Type to search (e.g. Aspirin)...",
        key="drug_b"
    )

# 5. INTERACTION LOGIC
if st.button("🔍 Check Compatibility", use_container_width=True):
    if drug_a and drug_b:
        if drug_a == drug_b:
            st.info("You have selected the same drug twice.")
        else:
            # Finding the match in JSON
            res = next((item for item in interactions if 
                        (item['drug1'] == drug_a and item['drug2'] == drug_b) or 
                        (item['drug1'] == drug_b and item['drug2'] == drug_a)), None)

            if res:
                if res['level'] == "RED":
                    st.error(f"### ❌ High Risk: {drug_a} + {drug_b}")
                    st.markdown(f"**Clinical Alert:** {res['message']}")
                elif res['level'] == "YELLOW":
                    st.warning(f"### ⚠️ Moderate Risk: {drug_a} + {drug_b}")
                    st.markdown(f"**Monitoring Required:** {res['message']}")
            else:
                st.success(f"### ✅ No Major Interaction Found")
                st.write(f"The combination of **{drug_a}** and **{drug_b}** appears safe based on our current database.")
    else:
        st.error("Please select both medications to run the check.")

# 6. FOOTER
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This tool is for academic purposes. Consult a registered medical practitioner before changing medication.")
