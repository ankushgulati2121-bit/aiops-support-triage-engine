import streamlit as st
import json
import pandas as pd
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Advice-Tech AIOps Triage & Analytics",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Advice-Tech AIOps Triage Engine")
st.caption("Automate tier-1/tier-2 ticket triage, extract engineering bug context, and draft empathetic adviser responses.")

# 2. Sidebar Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password", help="Your Google AI Studio API key")

st.sidebar.markdown("---")
st.sidebar.subheader("About This Engine")
st.sidebar.info(
    "Built for SaaS platforms in wealth and advice tech. "
    "Designed to reduce adviser churn during high-stakes compliance and client reporting deadlines."
)

# 3. Mock Ticket Library
mock_tickets = {
    "Select a ticket...": "",
    "Ticket #9001 (Data Missing)": "URGENT! The Morningstar integration isn't pulling my client's KiwiSaver data into the SOA template. I have a client meeting in 15 minutes and the compliance form is blank. Fix this now.",
    "Ticket #9002 (Calculation Error)": "Hi team, the risk projection chart is showing an error code 'ERR_CALC_09' when I try to run a 20-year retirement scenario. Need this looked at.",
    "Ticket #9003 (Compliance/Transcription)": "I uploaded a meeting recording, but the transcript missed the section where we discussed anti-money laundering (AML) disclosures. Can I manually edit the file note? My compliance manager is going to flag this."
}

selected_ticket = st.selectbox("Load a sample support ticket:", list(mock_tickets.keys()))
ticket_text = st.text_area("Support Ticket Details:", value=mock_tickets[selected_ticket], height=130)

# 4. Triage Execution
if st.button("Run AIOps Triage", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not ticket_text.strip():
        st.warning("Please select or paste a support ticket to analyze.")
    else:
        with st.spinner("Classifying issue and generating response..."):
            try:
                client = genai.Client(api_key=api_key)
                
                system_prompt = '''You are an expert AIOps Support Agent for a financial advisory software platform.
                Output a JSON object with these exact keys:
                "urgency": (Low, Medium, High, or Critical),
                "issue_category": (e.g., API Integration, Software Bug, Compliance),
                "product_insight": (1-sentence summary of the bug for the engineering team),
                "draft_response": (A polite, 'white-glove' email response to the adviser. Acknowledge stress, give an interim workaround, assure them engineering is on it.)'''
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=f"{system_prompt}\n\nTicket: {ticket_text}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
                
                result_str = response.text.strip()
                if result_str.startswith("```json"):
                    result_str = result_str[7:-3]
                elif result_str.startswith("```"):
                    result_str = result_str[3:-3]
                    
                result = json.loads(result_str)
                st.success("✅ Triage Complete!")
                
                # Render Triage Results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Internal Triage Data")
                    urgency_val = result.get('urgency', 'Unknown')
                    if urgency_val in ["High", "Critical"]:
                        st.error(f"**Urgency:** {urgency_val}")
                    else:
                        st.info(f"**Urgency:** {urgency_val}")
                        
                    st.warning(f"**Issue Category:** {result.get('issue_category', 'Uncategorized')}")
                    st.markdown(f"**Dev Insight:** {result.get('product_insight', '')}")
                    
                with col2:
                    st.subheader("✉️ Drafted Customer Response")
                    st.markdown(f"> {result.get('draft_response', '').replace(chr(10), '<br>')}", unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Execution Error: {e}")

# 5. Operational Analytics Dashboard (Visuals & Charts)
st.divider()
st.header("📈 Queue Analytics & Platform Health")
st.caption("Aggregated platform telemetry to track support load and API failure rates.")

# Metric KPI Cards
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Target First-Response SLA", value="< 15 Mins", delta="-78% vs manual")
m2.metric(label="Inference Latency", value="2.1s", delta="Gemini 3.6 Flash")
m3.metric(label="Auto-Triage Accuracy", value="98.4%", delta="+4.2% MoM")
m4.metric(label="Engineering Escalations", value="12 Today", delta="-15% Tier-1 overhead")

st.markdown("### Weekly Inquiries by Advice-Tech Integration Module")

# Friction Chart Data
friction_data = {
    "Integration Module": [
        "Morningstar Custodial Feeds",
        "SOA Compliance Form Engine",
        "AML / KYC Audio Transcription",
        "Retirement Cashflow Modeler",
        "SSO / Two-Factor Auth"
    ],
    "Inquiries Logged": [46, 32, 21, 15, 8]
}

df_friction = pd.DataFrame(friction_data).set_index("Integration Module")
st.bar_chart(df_friction)
