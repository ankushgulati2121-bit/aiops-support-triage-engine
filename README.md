# Advice-Tech AIOps Support Triage Engine
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11Azfr2iDL2-oE7HcK3FEA3HKSQLq86y3?usp=sharing)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aiops-support-triage-engine-juolynpyt2asqu4m6fbtei.streamlit.app/)
An operational AIOps workflow and interactive web dashboard built to automate tier-1/tier-2 ticket classification, extract technical bug summaries for engineering teams, and generate context-aware, white-glove drafted responses for financial advisers.

![Dashboard Preview]<img width="1238" height="562" alt="Demo" src="https://github.com/user-attachments/assets/317b1ccf-408a-40c9-9b6d-18b29dde7a7e" />


## Overview

In financial advice technology, adviser friction often stems from strict compliance deadlines (e.g., Statements of Advice, AML/KYC requirements) and third-party data integrations (e.g., Morningstar, custodial feeds). When critical workflows fail, support queues experience high-stress, unstructured inquiries.

This engine automates the operational triage pipeline:
- **Urgency & Severity Classification:** Dynamically flags high-stakes operational risks (e.g., pre-meeting compliance failures).
- **Engineering Bug Extraction:** Summarizes technical failure points into actionable Jira/Dev tickets without human manual entry.
- **Empathetic Draft Generation:** Drafts compliant, white-glove responses complete with immediate operational workarounds to reduce adviser downtime.

## Tech Stack

- **Frontend & App Framework:** Streamlit
- **Model Orchestration:** Google GenAI SDK (`gemini-3.6-flash`)
- **Language:** Python 3.10+
- **Data Serialization:** Strict JSON structured schema validation

## Repository Structure

```text
├── app.py              # Core Streamlit application and GenAI triage pipeline
├── requirements.txt    # Production dependency manifest
├── demo.png            # Application interface screenshot
└── README.md           # Documentation and architecture breakdown
