import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
from sklearn.preprocessing import LabelEncoder
import os

# Set page config
st.set_page_config(page_title="📊 AI Dashboard - Gemini Agents", layout="wide")
st.title("📊 AI-Powered Dashboard like Power BI")

# Configure Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "your API key")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# File Upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Global dictionary to store label encoders
label_encoders = {}

# Agent 2: Data Cleaning & Encoding
def agent_clean_data(df):
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.fillna(method='ffill').fillna(method='bfill')
    for col in df_cleaned.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df_cleaned[col] = le.fit_transform(df_cleaned[col].astype(str))
        label_encoders[col] = dict(zip(le.transform(le.classes_), le.classes_))
    return df_cleaned

# Agent to decode label-encoded values back for visualization
def revert_label_encoding(df_cleaned):
    df_reverted = df_cleaned.copy()
    for col, mapping in label_encoders.items():
        df_reverted[col] = df_reverted[col].map(mapping)
    return df_reverted

# KPI Card Function
def kpi_card(title, value, col):
    col.metric(label=title, value=f"{value:,.0f}")

# Dynamic Column Selector for Plotting
def plot_editor(df, plot_func, plot_title):
    st.markdown(f"#### ✏️ {plot_title} - Custom Editor")
    cols = df.columns.tolist()
    selected_cols = st.multiselect(f"Select columns for {plot_title}", cols, default=cols[:2], key=f"select_{plot_title}")
    if len(selected_cols) >= 1:
        plot_func(selected_cols)

# Agent 1: Dashboard Generator
def agent_generate_dashboard(df):
    st.subheader("📍 Auto-Generated Power BI Style Dashboard")
    numeric = df.select_dtypes(include=['int64', 'float64'])
    categorical = df.select_dtypes(include='object')

    # AI-generated Summary
    st.markdown("### 🧠 AI Summary")
    summary_prompt = f"Give a brief summary about this dataset: {df.describe(include='all').to_string()}"
    summary = model.generate_content(summary_prompt).text
    st.info(summary)

    # KPIs
    kpi_cols = numeric.columns[:4]
    st.markdown("### 🔢 Key Metrics")
    cols = st.columns(len(kpi_cols))
    for i, col_name in enumerate(kpi_cols):
        kpi_card(col_name, df[col_name].sum(), cols[i])

    # Top 5 by Count (Bar)
    st.markdown("### 📊 Top 5 Categories")
    def plot_top5(cols):
        for col in cols:
            fig = px.bar(df[col].value_counts().head(5), title=f"Top 5 - {col}", labels={"index": col, "value": "Count"})
            st.plotly_chart(fig, use_container_width=True)
    plot_editor(categorical, plot_top5, "Top 5 Categories")

    # Donut Chart
    st.markdown("### 🍩 Distribution by Category")
    def plot_donut(cols):
        for col in cols:
            donut_data = df[col].value_counts().reset_index()
            donut_data.columns = [col, 'count']
            fig = px.pie(donut_data, names=col, values='count', hole=0.5, title=f"{col} Distribution")
            st.plotly_chart(fig, use_container_width=True)
    plot_editor(categorical, plot_donut, "Donut Chart")

    # Correlation Heatmap
    st.markdown("### 🔥 Correlation Heatmap")
    if not numeric.empty:
        fig = px.imshow(numeric.corr(), text_auto=True, aspect="auto", title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)

    # Boxplots
    st.markdown("### 📦 Box Plots")
    def plot_box(cols):
        if len(cols) >= 2:
            for i in range(len(cols)-1):
                fig = px.box(df, x=cols[i], y=cols[i+1], title=f"{cols[i+1]} by {cols[i]}")
                st.plotly_chart(fig, use_container_width=True)
    plot_editor(df, plot_box, "Box Plot")

    # Pairplot-like Grid
    st.markdown("### 🔗 Feature Relationships")
    def plot_scatter_matrix(cols):
        fig = px.scatter_matrix(df, dimensions=cols)
        st.plotly_chart(fig, use_container_width=True)
    plot_editor(numeric, plot_scatter_matrix, "Feature Relationships")

# Main Execution
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(), use_container_width=True)

        with st.spinner("🤖 Agents cleaning data..."):
            df_clean = agent_clean_data(df)
            df_view = revert_label_encoding(df_clean)

        with st.spinner("📊 Generating dashboard..."):
            agent_generate_dashboard(df_view)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Upload a CSV file to generate the dashboard.")
