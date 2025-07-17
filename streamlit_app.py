import streamlit as st
import requests
import json
import pandas as pd

# Mock function to simulate fetching data from a database or API
def fetch_property_features(property_id):
    url = f"https://ap-southeast-2.api.vaultre.com.au/api/v1.3/properties/{property_id}/features"

    headers = {
        'Authorization': st.secrets["api"]["auth_token"],
        'x-api-key': st.secrets["api"]["api_key"]
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        rows = []
        for group in data["items"]:
            group_name = group["groupName"]
            feature_names = [feature["displayName"] for feature in group.get("features", [])]
            features_concatenated = ", ".join(feature_names)
            rows.append({"groupName": group_name, "features": features_concatenated})
    
        # Create DataFrame
        df = pd.DataFrame(rows)
    return df

# Streamlit UI
st.title("🏡 Property Feature Lookup")

property_id = st.text_input("Enter Property ID", placeholder="e.g., 30029515")

if st.button("Get Features"):
    if property_id:
        df = fetch_property_features(property_id.strip())
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No features found or invalid property ID.")
    else:
        st.warning("Please enter a Property ID.")
