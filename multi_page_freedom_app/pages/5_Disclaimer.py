# pages/5_Disclaimer.py
import streamlit as st
from data_utils import apply_dark_mode

st.title("Data Disclaimer")
template = apply_dark_mode()

st.markdown("""

## Disclaimer 
This application is provided for demonstration, educational, and informational purposes only.

The data presented in this application may be synthetic, aggregated, publicly available, outdated, incomplete, or subject to error, and should not be considered authoritative, official, or suitable for decision-making.

The creator makes no warranties or guarantees regarding the accuracy, completeness, reliability, or timeliness of the data or visualizations displayed.

This application does not represent any government agency, organization, or official institution, and the views and analyses expressed are solely those of the creator.

Users assume full responsibility for any use of the information provided. The creator shall not be held liable for any damages, losses, or claims arising from the use or misuse of this application or its contents.

## Data Source
Data used in this application originates from publicly available or third-party sources. All trademarks, data rights, and copyrights remain the property of their respective owners.

This project is not affiliated with, endorsed by, or sponsored by any data provider.

- Website : https://freedomhouse.org/report/freedom-world
- **Freedom House — Freedom in the World (FIW)** dataset (editions 2013–2025 in the provided sheet).
- Columns used include: *Total Score*, *Political Rights score*, *Civil Liberties score*, *Freedom Status*, *Region*, and others.

## Non-Commercial Use 
This application is a non-commercial portfolio project intended solely to demonstrate data analysis and visualization capabilities.

## No Professional Advice
Nothing in this application constitutes legal, medical, financial, or policy advice.

""")
