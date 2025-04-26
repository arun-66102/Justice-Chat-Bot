import streamlit as st
import pickle
import json
import time
import csv

# Load model (for future use, currently not applied in logic)
with open("justice_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load Justice database from JSON
json_file = "justice_data.json"
try:
    with open(json_file, 'r', encoding='utf-8') as file:
        justice_database = json.load(file)
except FileNotFoundError:
    st.error("❌ Justice data file not found!")
    justice_database = {}
except json.JSONDecodeError:
    st.error("❌ Error loading JSON data!")
    justice_database = {}

# Styling
st.markdown("""
    <style>
        h1 { text-align: center; font-size: 42px; font-weight: bold; color: #1b2e35; animation: fadeIn 2s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        .fadeIn { animation: fadeIn 1.5s; }
        .stButton>button {
            background: linear-gradient(to right, #4e54c8, #8f94fb);
            color: white; border: none; font-size: 16px;
            padding: 10px 14px; border-radius: 6px;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover { transform: scale(1.05); background: linear-gradient(to right, #8f94fb, #4e54c8); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="fadeIn">⚖️ Justice Chatbot</h1>', unsafe_allow_html=True)
st.write("Your digital legal assistant for justice-related services 🇮🇳")

# Input Fields
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Full Name")
    phone = st.text_input("📞 Phone Number")

with col2:
    location = st.text_input("📍 Your State/UT")
    query_type = st.selectbox("🔍 Query Type", ["SELECT"] + list(justice_database.keys()))

query_text = st.text_area("📝 Ask Your Question")

col1, col2 = st.columns(2)
with col1:
    submit = st.button("✅ Submit")
with col2:
    reset = st.button("🔄 Reset")

if reset:
    st.experimental_rerun()

if submit:
    with st.spinner("🔍 Fetching relevant legal information..."):
        time.sleep(2)

    errors = []
    if not name.strip():
        errors.append("❌ Full Name is required.")
    if not phone.strip() or len(phone) != 10 or not phone.isdigit():
        errors.append("❌ Enter a valid 10-digit phone number.")
    if query_type == "SELECT":
        errors.append("❌ Please select a valid Query Type.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        st.markdown('<h2 class="fadeIn">📋 Response from MYS Justice Chatbot:</h2>', unsafe_allow_html=True)
        responses = justice_database.get(query_type, ["❌ No data available for this query type."])
        for item in responses:
            st.success(f"🔹 {item}")

        # Save interaction to CSV
        record = {
            "name": name,
            "phone": phone,
            "location": location,
            "query_type": query_type,
            "query_text": query_text
        }

        csv_file = 'justice_queries.csv'
        try:
            with open(csv_file, mode='r'):
                file_exists = True
        except FileNotFoundError:
            file_exists = False

        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)

        with open(csv_file, "rb") as f:
            st.download_button("📥 Download Query Log", data=f, file_name=csv_file, mime="text/csv")