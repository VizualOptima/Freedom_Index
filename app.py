# importing dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import io

# st.set_page_config(page_title="Global Freedom Index Dashboard", layout="wide")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def data_load():
    url = "https://raw.githubusercontent.com/VizualOptima/Freedom_Index/main/All_data_FIW_2013-2024.xlsx"
    df = pd.read_excel(url, sheet_name="FIW13-25", header=1)

    # Standardize column names
    df = df.rename(columns={
        "Region": "Region",
        "Edition": "Year",
        "Status": "Freedom Status",
        "PR rating": "Political Rights ratings",
        "CL rating": "Civil Liberties ratings",
        "F": "Freedom Score ratings",
        "PR": "Political Rights score",
        "CL": "Civil Liberties score",
        "Total": "Total Score"
    })

    # Normalize types and values
    if "C/T" in df.columns:
        df["C/T"] = df["C/T"].replace({"c": "Country", "t": "Territory"})
    # Coerce numerics
    for col in ["Year", "Total Score", "Political Rights score", "Civil Liberties score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure country/territory name column exists
    if "Country/Territory" not in df.columns:
        # Try common alternatives if needed
        for alt in ["Country / Territory", "Country or Territory", "Country"]:
            if alt in df.columns:
                df = df.rename(columns={alt: "Country/Territory"})
                break

    return df

df_freedom = data_load()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Navigation and Filters")

dark = st.sidebar.toggle("Dark mode", value=False, key="dark_mode")
template = "plotly_dark" if dark else "plotly"

# Optional page-level CSS for background/text
if dark:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0b1220; color: #e5e7eb; }
        </style>
        """,
        unsafe_allow_html=True,
    )

color_scale = st.sidebar.selectbox(
    "Select Color Scale",
    ["viridis", "plasma", "inferno", "magma", "cividis", "RdYlGn", "Blues", "Greens", "Turbo", "IceFire"],
)

# Controls
ct_options = sorted(df_freedom["C/T"].dropna().unique().tolist(), reverse=True) if "C/T" in df_freedom.columns else []
country_or_territory = st.sidebar.selectbox("Country or Territory", ct_options) if ct_options else None

year_options = sorted(df_freedom["Year"].dropna().unique().tolist(), reverse=True)
year = st.sidebar.selectbox("Year", year_options, index=0 if year_options else None)

region = st.sidebar.multiselect("Region(s)", options=sorted(df_freedom["Region"].dropna().unique().tolist()))
freedom_status = st.sidebar.multiselect("Freedom Status", options=sorted(df_freedom["Freedom Status"].dropna().unique().tolist()))

# Slider bounds guarded for NaNs
min_score = float(df_freedom["Total Score"].min()) if df_freedom["Total Score"].notna().any() else 0.0
max_score = float(df_freedom["Total Score"].max()) if df_freedom["Total Score"].notna().any() else 100.0
score = st.sidebar.slider("Score Range", min_score, max_score, value=(min_score, max_score))

# -----------------------------
# Apply filters
# -----------------------------
df_filtered = df_freedom.copy()

if year is not None:
    df_filtered = df_filtered[df_filtered["Year"] == year]

df_filtered = df_filtered[df_filtered["Total Score"].between(score[0], score[1])]

if region:
    df_filtered = df_filtered[df_filtered["Region"].isin(region)]

if freedom_status:
    df_filtered = df_filtered[df_filtered["Freedom Status"].isin(freedom_status)]

if country_or_territory and "C/T" in df_filtered.columns:
    # FIX: selectbox returns a string; use equality (or wrap in a list for .isin)
    df_filtered = df_filtered[df_filtered["C/T"] == country_or_territory]

# -----------------------------
# Title & KPIs
# -----------------------------
st.title("Global Freedom Index Dashboard")
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

# -----------------------------
# Choropleth Map
# -----------------------------
st.subheader("Freedom Score Map")
if len(df_filtered) == 0:
    st.placeholder()
else:
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

# -----------------------------
# Line Chart Over Time
# -----------------------------
st.subheader("Score Trends by Country")
countries_all = sorted(df_freedom["Country/Territory"].dropna().unique().tolist())
selected_countries = st.multiselect("Select Countries", options=countries_all)

if selected_countries:
    df_trend = df_freedom[df_freedom["Country/Territory"].isin(selected_countries)].sort_values(["Country/Territory", "Year"])
    if len(df_trend) > 0:
        fig_line = px.line(
            df_trend,
            x="Year",
            y="Total Score",
            color="Country/Territory",
            markers=True,
            template=template,
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No data available for the selected countries.")

# -----------------------------
# Data Table + Download
# -----------------------------
st.subheader("Filtered Dataset")
st.dataframe(df_filtered)

if len(df_filtered) > 0:
    csv = df_filtered.to_csv(index=False)
    st.download_button("⬇️ Download CSV", data=csv, file_name="filtered_freedom_data.csv", mime="text/csv")
else:
    st.button("⬇️ Download CSV", disabled=True)
