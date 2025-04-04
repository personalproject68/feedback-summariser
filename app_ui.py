import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

st.title("📝 Feedback Portal")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Submit Feedback", "View Feedback", "Summaries"])

with tab1:
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

with tab2:
    st.subheader("📋 All Feedback")
    
    if st.button("Refresh Feedback", key="refresh_feedback"):
        st.experimental_rerun()
    
    resp = requests.get(f"{API_URL}/messages")
    if resp.status_code == 200:
        messages = resp.json()["messages"]
        
        # Add summarize button if there are messages
        if messages:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Generate Summary"):
                    with st.spinner("Analyzing feedback..."):
                        summary_resp = requests.post(f"{API_URL}/summarize")
                        if summary_resp.status_code == 200:
                            response_data = summary_resp.json()
                            st.success(f"✅ Summary generated!")
                            
                            # Display any warnings
                            if "warning" in response_data:
                                st.warning(response_data["warning"])
                            
                            # Display the summary in a nice format
                            with st.expander("View Generated Summary", expanded=True):
                                st.markdown("### Summary Analysis")
                                st.markdown(response_data["summary"].strip())
                                st.caption(f"Based on {response_data.get('feedback_count', 0)} feedback messages")
                        else:
                            error_detail = "Unknown error"
                            try:
                                error_data = summary_resp.json()
                                error_detail = error_data.get("detail", "Unknown error")
                            except:
                                error_detail = summary_resp.text or "Unknown error"
                            st.error(f"Failed to generate summary: {error_detail}")
        
        # Display messages
        st.markdown("### Recent Feedback")
        for item in messages:
            with st.expander(f"{item['name']} - {datetime.fromisoformat(item['created_at']).strftime('%Y-%m-%d %H:%M')}"):
                st.write(item["message"])
    else:
        st.error("Could not fetch messages.")

with tab3:
    st.subheader("📊 Feedback Summaries")
    
    if st.button("Refresh Summaries", key="refresh_summaries"):
        st.experimental_rerun()
    
    summaries_resp = requests.get(f"{API_URL}/summaries")
    if summaries_resp.status_code == 200:
        summaries = summaries_resp.json()["summaries"]
        for summary in summaries:
            with st.expander(f"Summary from {datetime.fromisoformat(summary['created_at']).strftime('%Y-%m-%d %H:%M')} ({summary.get('feedback_count', 0)} messages)"):
                # Display the summary in a cleaner format
                st.markdown("### Summary Analysis")
                st.markdown(summary["summary"].strip())
                
                # Show original feedback messages directly
                if "feedback_messages" in summary:
                    st.markdown("---")
                    st.markdown("### Original Feedback Messages")
                    for msg in summary["feedback_messages"]:
                        st.markdown(f"• {msg}")
    else:
        st.error("Could not fetch summaries.") 