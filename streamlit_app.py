import streamlit as st

# Mock function to simulate fetching data from a database or API
def fetch_property_data(property_id):
    mock_data = {
        "101": {"Address": "123 Main St", "City": "Mumbai", "Price": "₹1.2 Cr", "Bedrooms": 3, "Bathrooms": 2},
        "102": {"Address": "456 Park Ave", "City": "Delhi", "Price": "₹2.5 Cr", "Bedrooms": 4, "Bathrooms": 3},
        "103": {"Address": "789 Sea View", "City": "Goa", "Price": "₹3 Cr", "Bedrooms": 5, "Bathrooms": 4},
    }
    return mock_data.get(property_id)

# Streamlit UI
st.set_page_config(page_title="Property Lookup", layout="centered")

st.title("🏡 Property Lookup by ID")

property_id = st.text_input("Enter Property ID", placeholder="e.g., 101")

if st.button("Get Property Details"):
    if property_id:
        data = fetch_property_data(property_id.strip())
        if data:
            st.success("Property details found:")
            st.write("### 📋 Details")
            for key, value in data.items():
                st.write(f"**{key}:** {value}")
        else:
            st.error("Property ID not found. Please try another one.")
    else:
        st.warning("Please enter a Property ID.")
