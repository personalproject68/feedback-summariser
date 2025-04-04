import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("📝 Feedback Portal")

st.subheader("Submit Feedback")

name = st.text_input("Your Name")
message = st.text_area("Your Message")

if st.button("Submit"):
    if name and message:
        response = requests.post(f"{API_URL}/submit", json={"name": name, "message": message})
        if response.status_code == 200:
            st.success("Feedback submitted!")
        else:
            st.error("Submission failed.")
    else:
        st.warning("Please fill in all fields.")

st.divider()

st.subheader("📋 All Feedback")

resp = requests.get(f"{API_URL}/messages")
if resp.status_code == 200:
    for item in resp.json()["messages"]:
        st.markdown(f"**{item['name']}**: {item['message']}")
else:
    st.error("Could not fetch messages.") 