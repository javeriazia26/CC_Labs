"""Plotly charts."""
import plotly.express as px

COLORS = {"LOW": "#2ca02c", "MEDIUM": "#ff9800", "HIGH": "#d62728"}


def risk_pie(df):
    counts = df["risk_level"].value_counts().reset_index()
    counts.columns = ["risk_level", "count"]
    return px.pie(counts, names="risk_level", values="count", color="risk_level",
                  color_discrete_map=COLORS, title="Risk distribution", hole=0.4)


def score_bar(df):
    return px.bar(df, x="document_id", y="risk_score", color="risk_level",
                  color_discrete_map=COLORS, title="Risk score per document", range_y=[0, 100])
