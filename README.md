# Advice-Tech AIOps Support Triage Engine

An operational AIOps workflow and interactive web dashboard built to automate tier-1/tier-2 ticket classification, extract technical bug summaries for engineering teams, and generate context-aware, white-glove drafted responses for financial advisers.

![Dashboard Preview](demo.png)

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
