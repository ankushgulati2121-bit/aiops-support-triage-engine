import streamlit as st
import json
from google import genai
from google.genai import types

# 1. Setup the Web Page
st.set_page_config(page_title="AIOps Triage Engine", layout="wide")
st.title("🛠️ Advice-Tech AIOps Triage Engine")
st.markdown("Automatically categorize support tickets and draft white-glove responses.")

# 2. Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# 3. Mock Data
mock_tickets = {
    "Select a ticket...": "",
    "Ticket #9001 (Data Missing)": "URGENT! The Morningstar integration isn't pulling my client's KiwiSaver data into the SOA template. I have a client meeting in 15 minutes and the compliance form is blank. Fix this now.",
    "Ticket #9002 (Calculation Error)": "Hi team, the risk projection chart is showing an error code 'ERR_CALC_09' when I try to run a 20-year retirement scenario. Need this looked at.",
    "Ticket #9003 (Compliance/Transcription)": "I uploaded a meeting recording, but the transcript missed the section where we discussed anti-money laundering (AML) disclosures. Can I manually edit the file note? My compliance manager is going to flag this."
}

selected_ticket = st.selectbox("Load a sample support ticket:", list(mock_tickets.keys()))
ticket_text = st.text_area("Support Ticket Details:", value=mock_tickets[selected_ticket], height=150)

# 4. The AIOps Engine 
if st.button("Run AIOps Triage"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not ticket_text:
        st.warning("Please provide a support ticket to analyze.")
    else:
        with st.spinner("Analyzing ticket and drafting response..."):
            try:
                # Use the new Google GenAI SDK to handle AQ. keys
                client = genai.Client(api_key=api_key)
                
                system_prompt = '''You are an expert AIOps Support Agent for a financial advisory software platform.
                Output a JSON object with these exact keys:
                "urgency": (Low, Medium, High, or Critical),
                "issue_category": (e.g., API Integration, Software Bug, Compliance),
                "product_insight": (1-sentence summary of the bug for the engineering team),
                "draft_response": (A polite, 'white-glove' email response to the adviser. Acknowledge stress, give a workaround, assure them engineering is on it.)'''
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"{system_prompt}\n\nTicket: {ticket_text}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
                
                # Clean and load JSON safely
                result_str = response.text.strip()
                if result_str.startswith("```json"):
                    result_str = result_str[7:-3]
                elif result_str.startswith("```"):
                    result_str = result_str[3:-3]
                    
                result = json.loads(result_str)
                st.success("✅ Triage Complete!")
                
                # 5. Display Output
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Internal Triage Data")
                    st.info(f"**Urgency:** {result.get('urgency')}")
                    st.warning(f"**Issue Category:** {result.get('issue_category')}")
                    st.write(f"**Dev Insight:** {result.get('product_insight')}")
                    
                with col2:
                    st.subheader("✉️ Drafted Customer Response")
                    st.markdown(f"> {result.get('draft_response').replace(chr(10), '<br>')}", unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error: {e}")
