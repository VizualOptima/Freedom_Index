# pages/2_Country_or_Territory.py
import streamlit as st
import plotly.express as px
import pandas as pd

from data_utils import load_data, apply_dark_mode, color_scale_selector

st.sidebar.header("Country / Territory Filters")

df = load_data()
template = apply_dark_mode()
color_scale = color_scale_selector("Turbo")

st.title("Country / Territory Focus")

# Filters (Country/Territory name, Year, Region)
countries_all = sorted(df["Country/Territory"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Country or Territory", options=countries_all)

year_options = sorted(df["Year"].dropna().unique().tolist(), reverse=True)
year = st.sidebar.selectbox("Year", year_options, index=0 if year_options else None)

regions_all = sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region (optional)", options=["(All)"] + regions_all, index=0)

# Apply filters
df_year = df[df["Year"] == year] if year is not None else df.copy()
if selected_region != "(All)":
    df_year = df_year[df_year["Region"] == selected_region]

df_country_row = df_year[df_year["Country/Territory"] == selected_country]

# KPIs for the selected country/year
st.markdown(f"**Selected:** {selected_country} — {year}" + (f" — {selected_region}" if selected_region != "(All)" else ""))

k1, k2, k3 = st.columns(3)
if len(df_country_row) == 0:
    k1.metric("Total Score", "—")
    k2.metric("PR score", "—")
    k3.metric("CL score", "—")
    st.info("No row found for the chosen filters.")
else:
    row = df_country_row.iloc[0]
    k1.metric("Total Score", float(row.get("Total Score", float("nan"))))
    k2.metric("Political Rights", float(row.get("Political Rights score", float("nan"))))
    k3.metric("Civil Liberties", float(row.get("Civil Liberties score", float("nan"))))

# Score Trend (all years for selected country)
st.subheader("Score Trend Over Time")
df_trend = df[df["Country/Territory"] == selected_country].sort_values(["Year"])
if len(df_trend) > 0:
    fig_line = px.line(
        df_trend,
        x="Year",
        y="Total Score",
        markers=True,
        template=template,
        title=f"Total Score — {selected_country}",
    )
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("No trend data for this selection.")

# Single-country map (for visual location/context)
st.subheader("Map (Selected Country Highlight)")
df_map = df_year[df_year["Country/Territory"] == selected_country]
if len(df_map) > 0:
    fig_map = px.choropleth(
        df_map,
        locations="Country/Territory",
        locationmode="country names",
        color="Total Score",
        hover_name="Country/Territory",
        color_continuous_scale=color_scale,
        template=template,
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.empty()

# Filtered table (country-specific)
st.subheader("Filtered Dataset (Country)")
st.dataframe(df_map if len(df_map) > 0 else df_country_row, use_container_width=True)

if len(df_map) > 0 or len(df_country_row) > 0:
    export_df = df_map if len(df_map) > 0 else df_country_row
    csv = export_df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", data=csv, file_name=f"{selected_country}_{year}_freedom_data.csv", mime="text/csv")
else:
    st.button("⬇️ Download CSV", disabled=True)
