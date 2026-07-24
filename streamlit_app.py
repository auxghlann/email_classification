import os
from pathlib import Path
import re
from collections import Counter
import httpx
import pandas as pd
import streamlit as st

from app.services.classifier_service import get_classifier_service

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

SAMPLE_SPAM = (
    "Subject: Congratulations"
    "You won a free prize. Click here now for money cash dollar claim."
)

SAMPLE_HAM = (
    "Subject: Project Update Meeting. "
    "Hi team, please find attached the report for our weekly meeting. "
    "Let me know if you have any questions or feedback before tomorrow."
)

st.set_page_config(
    page_title="Email Classification System",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State
if "email_input" not in st.session_state:
    st.session_state["email_input"] = ""


def set_sample_spam() -> None:
    st.session_state["email_input"] = SAMPLE_SPAM


def set_sample_ham() -> None:
    st.session_state["email_input"] = SAMPLE_HAM


def clear_text_input() -> None:
    st.session_state["email_input"] = ""


# Sidebar Setup
with st.sidebar:
    st.title("System Status")
    
    # Check Backend API Availability
    api_online = False
    try:
        response = httpx.get(f"{API_BASE_URL}/", timeout=1.5)
        if response.status_code == 200:
            api_online = True
    except Exception:
        api_online = False

    if api_online:
        st.success("Backend API: Online (Connected)")
        st.caption(f"Target URL: {API_BASE_URL}/api/v1/classify")
    else:
        st.warning("Backend API: Offline")
        st.caption("Operating Mode: Local Classifier Service Fallback")

    st.markdown("---")
    st.subheader("Model Information")
    st.markdown("- **Algorithm**: Logistic Regression")
    st.markdown("- **Vocabulary Size**: 3,000 Words")
    st.markdown("- **Task**: Binary Email Spam Classification")


# Main Page Header
st.title("Email Classification Dashboard")
st.markdown(
    "Analyze email messages in real time using a pre-trained scikit-learn model. "
    "Enter raw email text below or select a sample payload to inspect prediction confidence and word features."
)

st.markdown("### Quick Pre-fill Samples")
col_s1, col_s2, col_s3, col_pad = st.columns([1.5, 1.5, 1, 4])

with col_s1:
    st.button("Load Sample Spam", on_click=set_sample_spam, use_container_width=True)

with col_s2:
    st.button("Load Sample Ham", on_click=set_sample_ham, use_container_width=True)

with col_s3:
    st.button("Clear Text", on_click=clear_text_input, use_container_width=True)


# Email Input Area
email_input = st.text_area(
    "Email Content Payload",
    height=180,
    placeholder="Paste or type raw email body text here...",
    key="email_input",
)


def classify_text(text: str):
    # Attempt via API first if online
    if api_online:
        try:
            resp = httpx.post(
                f"{API_BASE_URL}/api/v1/classify",
                json={"text": text},
                timeout=5.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["is_spam"], data["confidence"], "FastAPI REST Endpoint"
            elif resp.status_code == 400:
                raise ValueError(resp.json().get("detail", "Invalid input payload."))
        except httpx.HTTPError:
            pass  # Fall back to local service below

    # Local fallback
    service = get_classifier_service()
    res = service.classify(text)
    return res.is_spam, res.confidence, "Local Classifier Service"


# Classification Action
if st.button("Classify Email", type="primary", use_container_width=False):
    if not email_input or not email_input.strip():
        st.error("Email content cannot be empty or whitespace only. Please provide valid text.")
    else:
        with st.spinner("Analyzing email features and running inference..."):
            try:
                is_spam, confidence, provider = classify_text(email_input)
                
                st.markdown("---")
                st.subheader("Classification Results")

                res_col1, res_col2 = st.columns([2, 3])

                with res_col1:
                    if is_spam:
                        st.error("PREDICTION: SPAM DETECTED")
                    else:
                        st.success("PREDICTION: HAM / SAFE EMAIL")

                    st.caption(f"Inference Provider: {provider}")

                with res_col2:
                    st.metric(
                        label="Model Confidence Score",
                        value=f"{confidence * 100:.2f}%",
                    )
                    st.progress(float(confidence))

                # Word Feature Frequency Analysis
                st.markdown("### Vocabulary Feature Breakdown")
                service = get_classifier_service()
                words = re.findall(r"\b[a-zA-Z0-9]+\b", email_input.lower())
                word_counts = Counter(words)
                
                matched_features = [
                    {"Feature Word": w, "Occurrences": word_counts[w]}
                    for w in service.feature_names
                    if w in word_counts
                ]

                if matched_features:
                    df_features = pd.DataFrame(matched_features).sort_values(
                        by="Occurrences", ascending=False
                    )
                    st.dataframe(
                        df_features,
                        use_container_width=True,
                        hide_index=True,
                    )
                    st.caption(f"Total matching vocabulary features detected: {len(matched_features)}")
                else:
                    st.info("No matching vocabulary words from the 3,000-word feature set were found in this text.")

            except Exception as e:
                st.error(f"Classification failed: {str(e)}")
