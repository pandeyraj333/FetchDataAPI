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
            'displayAddress': data['displayAddress'],
            'saleLifeId': data['saleLifeId'],
            'bed': data['bed'],
            'bath': data['bath'],
            'garages': data['garages'],
            'carports': data['carports'],
            'openSpaces': data['openSpaces'],
            'ensuites': data['ensuites'],
            'toilets': data['toilets'],
            'floorArea': data['floorArea']['value'],
            'landArea': data['landArea']['value'],
            'receptionRooms': data['receptionRooms'],
            'yearBuilt': data['yearBuilt'],
            'lotNumber': data['lotNumber'],
            'rpdp': data['rpdp'],
            'certificateOfTitle': data['certificateOfTitle'],
            'legalDescription': data['legalDescription'],
            'landValue': data['landValue'],
            'improvementValue': data['improvementValue'],
            'rateableValue': data['rateableValue'],
            'Council':  data['rates']['council']['value'],
            'methodOfSale': data['methodOfSale'],
            'heading': data['heading'],
            'description': data['description'],
            'internalRemarks': data['internalRemarks'],
            'editableBy':  data['editableBy'][0]['name']
        })
        
        df = pd.DataFrame(rows)
    return df


# Streamlit UI
st.title(f"🏡 Property Feature Lookup token:{st.secrets["api"]["auth_token"]} Key: {st.secrets["api"]["api_key"]}")

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
