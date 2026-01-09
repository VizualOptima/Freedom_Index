# pages/3_Methodology.py
import streamlit as st
from data_utils import apply_dark_mode

st.title("Methodology")
template = apply_dark_mode()

st.markdown("""
## Data Source
- **Freedom House — Freedom in the World (FIW)** dataset (editions 2013–2025 in the provided sheet).
- Columns used include: *Total Score*, *Political Rights score*, *Civil Liberties score*, *Freedom Status*, *Region*, and others.

## Scoring
- **Total Score**: Composite of Political Rights (PR) and Civil Liberties (CL) indicators.
- **Political Rights score (PR)** and **Civil Liberties score (CL)**: Aggregated sub-indices per Freedom House definitions.
- **Freedom Status**: Categorization (e.g., *Free*, *Partly Free*, *Not Free*) based on thresholds applied to PR/CL results.

## Processing Steps
1. Load Excel sheet `FIW13-25` with header at row 2 (index 1).
2. Standardize key column names; coerce numeric fields: *Year*, *Total Score*, *PR score*, *CL score*.
3. Normalize the `C/T` flag to human-readable labels: *Country* vs *Territory*.
4. Ensure the entity column is `Country/Territory` (fallback to common alternatives if needed).
5. Filters are applied in this order on the **Overview** page:
   - Year → Score Range → Region(s) → Freedom Status → C/T.
6. **Country / Territory Focus** page filters the dataset by *Country/Territory*, *Year*, and optional *Region*; trend lines use **all years** for the chosen entity.

## Map Rendering
- The choropleth uses Plotly with `locationmode="country names"`. Country naming consistency is assumed to match Plotly’s built-in country resolver.

## Notes & Limitations
- Name mismatches (e.g., territories or partially recognized states) may not map on the choropleth.
- Some years may have missing scores; numeric coercion sets non-numeric values to NaN and thus excludes them from aggregates.
- If Freedom House updates the methodology or thresholds, interpretations across years should be contextualized accordingly.
""")
