import streamlit as st

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
st.set_page_config(page_title="Property Lookup", layout="centered")

st.title("🏡 Property Lookup by ID")

property_id = st.text_input("Enter Property ID", placeholder="e.g., 101")

if st.button("Get Property Features Details"):
    if property_id:
        data = fetch_property_features(property_id.strip())
        if data:
            st.success("Property details found:")
            st.write("### 📋 Details")
            for key, value in data.items():
                st.write(f"**{key}:** {value}")
        else:
            st.error("Property ID not found. Please try another one.")
    else:
        st.warning("Please enter a Property ID.")
