# pages/4_Glossary.py
import streamlit as st
from data_utils import apply_dark_mode

st.title("Glossary")
template = apply_dark_mode()

st.markdown("""
**Country/Territory (C/T)**  
Indicates whether an entry is a fully recognized country or a territory.

**Edition (Year)**  
The Freedom in the World report year corresponding to the assessment period.

**Freedom Status**  
Categorical label (e.g., *Free*, *Partly Free*, *Not Free*) determined by PR and CL results.

**Political Rights (PR)**  
Measures electoral process, political pluralism and participation, and functioning of government.

**Civil Liberties (CL)**  
Measures freedom of expression and belief, associational and organizational rights, rule of law, and personal autonomy and individual rights.

**Total Score**  
Composite metric combining PR and CL components; used to compare entities overall.

**Region**  
Geographic grouping used for regional comparisons and aggregation.

**Score Trend**  
Year-over-year evolution of **Total Score** for a given country/territory.

**Choropleth Map**  
A thematic map that uses color to represent a numeric variable (here: *Total Score*) across countries.

**NaN (Not a Number)**  
Represents missing or non-numeric values after coercion during data cleaning.
""")
