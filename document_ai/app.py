"""Streamlit dashboard. Run:  streamlit run dashboard/app.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so 'dashboard' imports work

import pandas as pd
import requests
import streamlit as st
from dashboard.charts import risk_pie, score_bar

st.set_page_config(page_title="Secure Document AI", layout="wide")
st.title("🔒 Secure Document AI")
st.caption("Authenticity / Tampering Risk Analysis — indicators only, not proof of forgery.")

api = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000")
files = st.file_uploader("Upload documents", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("Analyze", type="primary") and files:
    with st.spinner("Analyzing..."):
        try:
            up = requests.post(f"{api}/upload",
                               files=[("files", (f.name, f.getvalue())) for f in files], timeout=60)
            up.raise_for_status()
            for item in up.json():
                requests.post(f"{api}/analyze/{item['document_id']}", timeout=180).raise_for_status()
            st.success(f"Analyzed {len(files)} document(s)")
        except Exception as e:
            st.error(f"Backend error: {e}")

try:
    docs = [d for d in requests.get(f"{api}/documents", timeout=10).json() if d["result"]]
except Exception:
    st.warning("Backend not reachable. Start it with: uvicorn backend.main:app --reload")
    st.stop()

if not docs:
    st.info("No analyzed documents yet. Upload some above.")
    st.stop()

rows = []
for d in docs:
    r = d["result"]
    rows.append({"document_id": r["document_id"], "filename": r["filename"], "type": r["document_type"],
                 "ocr_conf": r["ocr_confidence"], "ai_prob": r["security"]["ai_probability"],
                 "tamper": r["security"]["tamper_score"], "risk_score": r["security"]["risk_score"],
                 "risk_level": r["security"]["risk_level"], "validation": r["validation"]["status"]})
df = pd.DataFrame(rows)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Documents", len(df))
c2.metric("Safe (LOW)", int((df.risk_level == "LOW").sum()))
c3.metric("Suspicious (MEDIUM)", int((df.risk_level == "MEDIUM").sum()))
c4.metric("High risk", int((df.risk_level == "HIGH").sum()))

left, right = st.columns(2)
left.plotly_chart(risk_pie(df), use_container_width=True)
right.plotly_chart(score_bar(df), use_container_width=True)
st.dataframe(df, use_container_width=True)

st.subheader("Document analysis")
choice = st.selectbox("Select document", df["document_id"])
r = next(d["result"] for d in docs if d["document_id"] == choice)
s, v = r["security"], r["validation"]

a, b = st.columns(2)
with a:
    st.markdown(f"**Type:** {r['document_type']} ({r['classification_confidence']:.0%})")
    st.markdown(f"**OCR confidence:** {r['ocr_confidence']:.0%}")
    st.markdown(f"**AI-likeness probability:** {s['ai_probability']:.0%}")
    st.markdown(f"**Tamper score:** {s['tamper_score']:.0%}")
    st.markdown(f"**Risk:** {s['risk_score']}/100 — **{s['risk_level']}**")
    for reason in s["reasons"]:
        st.warning(reason)
with b:
    st.markdown("**Extracted entities** (CNIC masked)")
    st.table(pd.DataFrame(r["entities"].items(), columns=["field", "value"]).astype(str))
    st.markdown(f"**Validation:** {v['status']}")
    for e in v["errors"]:
        st.error(e)
    for w in v["warnings"]:
        st.warning(w)
