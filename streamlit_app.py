import streamlit as st
import requests
import json
import pandas as pd

# Mock function to simulate fetching data from a database or API
def fetch_property_features(auth_token, api_key, property_id):
    url = f"https://ap-southeast-2.api.vaultre.com.au/api/v1.3/properties/{property_id}/features"

    headers = {
        'Authorization': auth_token #st.secrets["api"]["auth_token"],
        'x-api-key': api_key #st.secrets["api"]["api_key"]
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
        dataframe = pd.DataFrame(rows)
    return dataframe

def fetch_property_details(auth_token, api_key, property_id):
    url = f"https://ap-southeast-2.api.vaultre.com.au/api/v1.3/properties/residential/sale/{property_id}"
    headers = {
        'Authorization': auth_token #st.secrets["api"]["auth_token"],
        'x-api-key': api_key #st.secrets["api"]["api_key"]
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        rows = []
        rows.append({
            'displayAddress': data.get('displayAddress'),
            'saleLifeId': data.get('saleLifeId'),
            'bed': data.get('bed'),
            'bath': data.get('bath'),
            'garages': data.get('garages'),
            'carports': data.get('carports'),
            'openSpaces': data.get('openSpaces'),
            'ensuites': data.get('ensuites'),
            'toilets': data.get('toilets'),
            'floorArea': data.get('floorArea', {}).get('value'),
            'landArea': data.get('landArea', {}).get('value'),
            'receptionRooms': data.get('receptionRooms'),
            'yearBuilt': data.get('yearBuilt'),
            'lotNumber': data.get('lotNumber'),
            'rpdp': data.get('rpdp'),
            'certificateOfTitle': data.get('certificateOfTitle'),
            'legalDescription': data.get('legalDescription'),
            'landValue': data.get('landValue'),
            'improvementValue': data.get('improvementValue'),
            'rateableValue': data.get('rateableValue'),
            'Council': data.get('rates', {}).get('council', {}).get('value'),
            'methodOfSale': data.get('methodOfSale'),
            'heading': data.get('heading'),
            'description': data.get('description'),
            'internalRemarks': data.get('internalRemarks'),
            'editableBy': data.get('editableBy', [{}])[0].get('name')
        })

        df = pd.DataFrame(rows)
        return df

    else:
        st.error(f"API request failed: {response.status_code} - {response.text}")
        return None


def attach_tables(df_main, df_features_raw):
    # Pivot the features table (groupName becomes columns)
    df_features = df_features_raw.set_index("groupName").T.reset_index(drop=True)

    # Combine horizontally (same as pd.concat with axis=1)
    combined_df = pd.concat([df_main.reset_index(drop=True), df_features], axis=1)

    return combined_df



# Streamlit UI
st.title(f"🏡 Property Feature Lookup")

property_id = st.text_input("Enter Property ID", placeholder="e.g., 30029515")
auth_token = st.text_input("Enter Authorization Token")
api_key = st.text_input("Enter API Key")

if st.button("Get Details"):
    if property_id:
        df = fetch_property_details(auth_token.strip(), api_key.strip(), property_id.strip())
        df2 = fetch_property_features(auth_token.strip(), api_key.strip(), property_id.strip())
        df_attached = attach_tables(df,df2)
        if df_attached is not None and not df_attached.empty:
            st.dataframe(df_attached, use_container_width=True)
        else:
            st.warning("No Details found or invalid property ID.")
    else:
        st.warning("Please enter a Property ID.")
