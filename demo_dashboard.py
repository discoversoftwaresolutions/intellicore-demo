#!/usr/bin/env python3
"""
dashboard.py

Streamlit demo for Alibi-Detect IForest anomaly detection.
Requires: streamlit, numpy, pandas, alibi-detect
"""

import streamlit as st
import pandas as pd
import numpy as np
from alibi_detect.od import IForest

@st.cache_resource
def load_detector():
    """
    Initialize or load your trained IForest detector.
    For production, replace this with model.load(...).
    """
    return IForest()  # default, untrained forest

def main():
    st.set_page_config(page_title="Anomaly Detection Demo", layout="wide")
    st.title("📊 Alibi-Detect IForest Streamlit Demo")

    # Sidebar controls
    st.sidebar.header("Configuration")
    threshold = st.sidebar.slider(
        "Anomaly threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.01
    )
    uploaded = st.sidebar.file_uploader(
        "Upload CSV data", type=["csv"], help="Rows × features, no label column"
    )

    detector = load_detector()

    if uploaded:
        df = pd.read_csv(uploaded)
        st.subheader("Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Convert dataframe to numpy array
        X = df.to_numpy()

        with st.spinner("Running anomaly detection…"):
            preds = detector.predict(X, threshold=threshold)

        # Extract scores and labels
        scores = preds["data"]["score"]
        is_outlier = preds["data"]["is_outlier"]

        # Append results
        df["anomaly_score"] = np.round(scores, 4)
        df["is_anomaly"] = is_outlier.astype(int)

        st.subheader("Results")
        st.dataframe(df, use_container_width=True)

        # Simple chart of scores
        st.subheader("Score Distribution")
        st.bar_chart(df["anomaly_score"])

        st.success("Done!")
    else:
        st.info("📂 Please upload a CSV file to get started.")

if __name__ == "__main__":
    main()
