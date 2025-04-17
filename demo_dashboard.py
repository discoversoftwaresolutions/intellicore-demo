#!/usr/bin/env python3
"""
dashboard.py

Streamlit demo for Alibi-Detect IForest anomaly detection.
"""

import streamlit as st
import pandas as pd
import numpy as np
from alibi_detect.od import IForest
from pathlib import Path

DATA_DIR    = Path(__file__).parent / "data"
EXAMPLE_CSV = DATA_DIR / "example.csv"

@st.cache_resource
def load_detector():
    return IForest()

def main():
    st.set_page_config(page_title="Anomaly Demo", layout="wide")
    st.title("📊 Alibi-Detect IForest Demo")

    st.sidebar.header("Options")
    threshold   = st.sidebar.slider("Anomaly threshold", 0.0, 1.0, 0.5, 0.01)
    use_example = st.sidebar.checkbox("Use example dataset", value=False)
    uploaded    = st.sidebar.file_uploader("Upload CSV", type=["csv"], disabled=use_example)

    if use_example:
        if not EXAMPLE_CSV.exists():
            st.error(f"No example.csv found at {EXAMPLE_CSV}")
            return
        df = pd.read_csv(EXAMPLE_CSV)
    elif uploaded:
        df = pd.read_csv(uploaded)
    else:
        st.info("Please upload a CSV or select the example dataset.")
        return

    st.subheader("Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    X = df.to_numpy()
    detector = load_detector()
    with st.spinner("Detecting anomalies…"):
        preds = detector.predict(X, threshold=threshold)

    df["anomaly_score"] = np.round(preds["data"]["score"], 4)
    df["is_anomaly"]    = preds["data"]["is_outlier"].astype(int)

    st.subheader("Results")
    st.dataframe(df, use_container_width=True)

    st.subheader("Score Distribution")
    st.bar_chart(df["anomaly_score"])

if __name__ == "__main__":
    main()
