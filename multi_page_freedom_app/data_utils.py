# data_utils.py
import streamlit as st
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/VizualOptima/Freedom_Index/main/All_data_FIW_2013-2024.xlsx"
SHEET = "FIW13-25"

@st.cache_data
def load_data(url: str = DATA_URL, sheet_name: str = SHEET) -> pd.DataFrame:
    df = pd.read_excel(url, sheet_name=sheet_name, header=1)

    # Standardize column names (keep your existing mapping)
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

    # Normalize "C/T"
    if "C/T" in df.columns:
        df["C/T"] = df["C/T"].replace({"c": "Country", "t": "Territory"})

    # Coerce numerics
    for col in ["Year", "Total Score", "Political Rights score", "Civil Liberties score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure Country/Territory column exists
    if "Country/Territory" not in df.columns:
        for alt in ["Country / Territory", "Country or Territory", "Country"]:
            if alt in df.columns:
                df = df.rename(columns={alt: "Country/Territory"})
                break

    return df

def apply_dark_mode():
    dark = st.sidebar.toggle("Dark mode", value=st.session_state.get("dark_mode", False), key="dark_mode")
    if dark:
        st.markdown(
            """
            <style>
            .stApp { background-color: #0b1220; color: #e5e7eb; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    return "plotly_dark" if dark else "plotly"

def color_scale_selector(default: str = "viridis") -> str:
    return st.sidebar.selectbox(
        "Select Color Scale",
        ["viridis", "plasma", "inferno", "magma", "cividis", "RdYlGn", "Blues", "Greens", "Turbo", "IceFire"],
        index=["viridis","plasma","inferno","magma","cividis","RdYlGn","Blues","Greens","Turbo","IceFire"].index(default),
    )
