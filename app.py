import streamlit as st
import json

# 1. LOAD DATA WITH SAFETY
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load database: {e}")
        return []

interactions = load_data()

# 2. AUTOMATIC DRUG LIST GENERATION
# This gathers all drugs from 'drug1' and 'drug2' columns in your JSON
all_drugs = set()
for item in interactions:
    all_drugs.add(item['drug1'])
    all_drugs.add(item['drug2'])
drug_options = sorted(list(all_drugs))

# 3. UI DESIGN
st.set_page_config(page_title="DDI Checker India", page_icon="💊", layout="centered")

st.title("💊 Indian Drug Interaction Checker")
st.info("Select two medications to check for potential safety risks.")

# 4. THE SMART SELECT BOXES
col1, col2 = st.columns(2)

with col1:
    drug_a = st.selectbox(
        "First Drug",
        options=drug_options,
        index=None,
        placeholder="Type to search..."
    )

with col2:
    drug_b = st.selectbox(
        "Second Drug",
        options=drug_options,
        index=None,
        placeholder="Type to search..."
    )

# 5. CHECK LOGIC
if st.button("Check Interaction", use_container_width=True):
    if drug_a and drug_b:
        if drug_a == drug_b:
            st.warning("Same medication selected. No interaction found.")
        else:
            # Search logic (checks both A+B and B+A)
            match = next((i for i in interactions if 
                         (i['drug1'] == drug_a and i['drug2'] == drug_b) or 
                         (i['drug1'] == drug_b and i['drug2'] == drug_a)), None)
            
            if match:
                if match['level'] == "RED":
                    st.error(f"### ❌ {match['level']}: DANGEROUS")
                else:
                    st.warning(f"### ⚠️ {match['level']}: CAUTION")
                st.subheader("Why?")
                st.write(match['message'])
            else:
                st.success("### ✅ Safe Combination")
                st.write(f"No major interaction documented between **{drug_a}** and **{drug_b}** in our list.")
    else:
        st.error("Please select two drugs first!")

st.markdown("---")
st.caption("Educational tool only. Always follow your doctor's prescription.")
