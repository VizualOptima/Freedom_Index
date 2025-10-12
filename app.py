# importing dependencies

import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Global Freedom Index Dashboard", layout="wide")

# Load data
@st.cache_data
def data_load():
    # Importing dataset
    freedom_index_url_data = "https://raw.githubusercontent.com/VizualOptima/Freedom_Index/main/All_data_FIW_2013-2024.xlsx"
    df_freedom = pd.read_excel(freedom_index_url_data)

    # Rename columns for better understanding
    df_freedom = df_freedom.rename(columns={
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
    '''
    renaming the values c as Country and t as territory
    '''
    df_freedom["C/T"] = df_freedom["C/T"].replace({'c':'Country','t':'Territory'})
    df_freedom["Year"] = pd.to_numeric(df_freedom["Year"],errors="coerce")
    df_freedom["Total Score"] = pd.to_numeric(df_freedom["Total Score"],errors="coerce")
df_freedom = data_load()

# Filters

#adding min and max for slider
min_score = int(df_freedom["Total Score"].min())
max_score = int(df_freedom["Total Score"].max())

'''
Keep this section to add slider for PL scores and CL scores
'''

#filter
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

color_scale = st.sidebar.selectbox("Select Color Scale",["viridis", "plasma", "inferno", "magma", "cividis",
     "RdYlGn", "Blues", "Greens", "Turbo", "IceFire"])
year = st.sidebar.selectbox("Year",sorted(df_freedom["Year"].unique(),reverse=True))
region = st.sidebar.multiselect("Region(s)", options=df_freedom["Region"].dropna().unique())
freedom_status = st.sidebar.multiselect("Freedom Status",options=df_freedom["Freedom Status"].dropna().unique())
score = st.sidebar.slider("Score Range",min_score,max_score,value=(min_score,max_score))

#applying filters
df_filtered = df_freedom[(df_freedom["Year"] == year)&(df_freedom["Total Score"].between(score[0], score[1]))]
if region:
    df_filtered = df_filtered[df_filtered["Region"].isin(region)]
if freedom_status:
    df_filtered = df_filtered[df_filtered["Freedom_Status"].isin(freedom_status)]

#Title and KPI
st.title("Global Freedom Index Dashboard")
st.markdown(f"**Year Selected:**{year}")

#setting columns for KPI
col1,col2,col3,col4 = st.columns(4)
col1.metric("Average Score", round(df_filtered["Total_Score"].mean(), 2))
col2.metric("Countries", df_filtered["Country"].nunique())
col3.metric("Max Score", df_filtered["Total_Score"].max())
col4.metric("Min Score", df_filtered["Total_Score"].min())

#Map
st.subheader("Freedom Score Map")
fig = px.choropleth(df_filtered, locations="Country", locationmode="country names",
                        color="Total_Score", hover_name="Country",
                        color_continuous_scale=color_scale, title="")
st.plotly_chart(fig, use_container_width=True)

# Line Chart Over Time
st.subheader("Score Trends by Country")
selected_countries = st.multiselect("Select Countries", options=df_freedom["Country"].unique())
if selected_countries:
    df_trend = df_freedom[df_freedom["Country"].isin(selected_countries)]
    fig_line = px.line(df_trend, x="Year", y="Total_Score", color="Country", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# Data Table + Download
st.subheader("Filtered Dataset")
st.dataframe(df_filtered)

csv = df_filtered.to_csv(index=False)
st.download_button("⬇️ Download CSV", data=csv, file_name="filtered_freedom_data.csv", mime="text/csv")