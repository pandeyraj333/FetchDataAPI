import streamlit as st
import requests
import json
import pandas as pd

# Mock function to simulate fetching data from a database or API
def fetch_property_features(property_id):
    url = f"https://ap-southeast-2.api.vaultre.com.au/api/v1.3/properties/residential/sale/{property_id}"

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
        dataframe = pd.DataFrame(rows)
    return dataframe

def fetch_property_details(property_id):
    url = f"https://ap-southeast-2.api.vaultre.com.au/api/v1.3/properties/{property_id}/features"

    headers = {
        'Authorization': st.secrets["api"]["auth_token"],
        'x-api-key': st.secrets["api"]["api_key"]
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



# Streamlit UI
st.title(f"🏡 Property Feature Lookup")

property_id = st.text_input("Enter Property ID", placeholder="e.g., 30029515")

if st.button("Get Details"):
    if property_id:
        df = fetch_property_details(property_id.strip())
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No Details found or invalid property ID.")
    else:
        st.warning("Please enter a Property ID.")

if st.button("Get Features"):
    if property_id:
        df = fetch_property_features(property_id.strip())
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No features found or invalid property ID.")
    else:
        st.warning("Please enter a Property ID.")
