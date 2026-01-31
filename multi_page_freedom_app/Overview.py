# app.py
import streamlit as st
import plotly.express as px
import pandas as pd

from data_utils import load_data, apply_dark_mode, color_scale_selector

st.set_page_config(page_title="Global Freedom Index Dashboard", layout="wide")
st.sidebar.header("Navigation and Filters")

# Load data
df_freedom = load_data()

# Theme + color scale
template = apply_dark_mode()
color_scale = color_scale_selector()

# Sidebar filters
ct_options = sorted(df_freedom["C/T"].dropna().unique().tolist(), reverse=True) if "C/T" in df_freedom.columns else []
country_or_territory = st.sidebar.selectbox("Country or Territory (type)", ct_options) if ct_options else None

year_options = sorted(df_freedom["Year"].dropna().unique().tolist(), reverse=True)
year = st.sidebar.selectbox("Year", year_options, index=0 if year_options else None)

region = st.sidebar.multiselect("Region(s)", options=sorted(df_freedom["Region"].dropna().unique().tolist()))
freedom_status = st.sidebar.multiselect("Freedom Status", options=sorted(df_freedom["Freedom Status"].dropna().unique().tolist()))

min_score = float(df_freedom["Total Score"].min()) if df_freedom["Total Score"].notna().any() else 0.0
max_score = float(df_freedom["Total Score"].max()) if df_freedom["Total Score"].notna().any() else 100.0
score = st.sidebar.slider("Score Range", min_score, max_score, value=(min_score, max_score))

# Apply filters
df_filtered = df_freedom.copy()
if year is not None:
    df_filtered = df_filtered[df_filtered["Year"] == year]

df_filtered = df_filtered[df_filtered["Total Score"].between(score[0], score[1])]

if region:
    df_filtered = df_filtered[df_filtered["Region"].isin(region)]

if freedom_status:
    df_filtered = df_filtered[df_filtered["Freedom Status"].isin(freedom_status)]

if country_or_territory and "C/T" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["C/T"] == country_or_territory]

# Title & KPIs
st.title("Global Freedom Index Dashboard — Overview")
st.markdown(f"**Year Selected:** {year}")

col1, col2, col3, col4 = st.columns(4)
if len(df_filtered) == 0:
    col1.metric("Average Score", "—")
    col2.metric("Countries", "0")
    col3.metric("Max Score", "—")
    col4.metric("Min Score", "—")
    st.info("No rows match your current filters. Try broadening the score range, clearing regions, or switching year.")
else:
    col1.metric("Average Score", round(df_filtered["Total Score"].mean(), 2))
    col2.metric("Countries", df_filtered["Country/Territory"].nunique())
    col3.metric("Max Score", float(df_filtered["Total Score"].max()))
    col4.metric("Min Score", float(df_filtered["Total Score"].min()))

# Choropleth Map
st.subheader("Freedom Score Map")
if len(df_filtered) > 0:
    fig = px.choropleth(
        df_filtered,
        locations="Country/Territory",
        locationmode="country names",
        color="Total Score",
        hover_name="Country/Territory",
        color_continuous_scale=color_scale,
        title="",
        template=template,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.empty()

# Data Table + Download
st.subheader("Filtered Dataset")
st.dataframe(df_filtered, use_container_width=True)

if len(df_filtered) > 0:
    csv = df_filtered.to_csv(index=False)
    st.download_button("⬇️ Download CSV", data=csv, file_name="filtered_freedom_data.csv", mime="text/csv")
else:
    st.button("⬇️ Download CSV", disabled=True)
