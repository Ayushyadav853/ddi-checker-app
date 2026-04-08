import streamlit as st
import json

# Load the data
with open('data.json') as f:
    interactions = json.load(f)

# List of drugs for the dropdown (simplified for now)
drug_list = sorted(list(set([i['drug1'] for i in interactions] + [i['drug2'] for i in interactions])))

st.set_page_config(page_title="DDI Checker", page_icon="💊")

st.title("💊 Visual Drug Interaction Checker")
st.write("Select two medications to check for potential interactions.")

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    drug_a = st.selectbox("Select Drug A", [""] + drug_list)

with col2:
    drug_b = st.selectbox("Select Drug B", [""] + drug_list)

if st.button("Check Interaction"):
    if drug_a and drug_b:
        if drug_a == drug_b:
            st.warning("Please select two different drugs.")
        else:
            # Search logic
            res = next((item for item in interactions if 
                        (item['drug1'] == drug_a and item['drug2'] == drug_b) or 
                        (item['drug1'] == drug_b and item['drug2'] == drug_a)), None)

            if res:
                if res['level'] == "RED":
                    st.error(f"### ❌ Interaction: {res['level']}")
                elif res['level'] == "YELLOW":
                    st.warning(f"### ⚠️ Interaction: {res['level']}")
                
                st.subheader("Explanation:")
                st.write(res['message'])
            else:
                st.success("### ✅ Safe Combination")
                st.write("No major interactions found in our database.")
    else:
        st.info("Please select both drugs to continue.")

st.divider()
st.caption("Disclaimer: For educational purposes only. Always consult a doctor.")
