import streamlit as st
import requests

st.title("🍲 Recipe Assistant")

query = st.text_input("Ask me for a recipe...")

if st.button("Get Recipe") and query:
    with st.spinner("Fetching..."):
        response = requests.post(
            "http://127.0.0.1:8000/generate_recipe", 
            json={"query": query}
        )
        if response.status_code == 200:
            result = response.json()
            st.markdown("### 🍽️ Result:")
            st.markdown(result["response"])  
        else:
            st.error("Something went wrong 😢")
