import streamlit as st
import os
from io import BytesIO
from citation_map import generate_citation_map

def clear_session():
    # Clear session state variables
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Set a query parameter to trigger refresh
    st.query_params.refresh = 'true'
    
# Streamlit app title
st.title("Google Scholar Citation World Map Generator")

# Scholar ID input
scholar_id = st.text_input("Enter your Google Scholar ID:")

# Output settings
output_path = st.text_input("HTML Output Path:", value="citation_map.html")
csv_output_path = st.text_input("CSV Output Path:", value="citation_info.csv")

# Map options
pin_colorful = st.checkbox("Colorful Pins", value=True)
affiliation_conservative = st.checkbox("Use Conservative Affiliation Identification", value=False)

# Number of processes for parallel processing
num_processes = st.number_input("Number of Processes", min_value=1, max_value=64, value=16)

# Proxy option
use_proxy = st.checkbox("Use Proxy (for environments with blocks)", value=False)

# Button to trigger map generation
if st.button("Generate Citation Map"):
    # Validate input
    if scholar_id:
        st.write("Generating citation map... Please wait.")
        
        # Call the function to generate the citation map
        generate_citation_map(
            scholar_id=scholar_id,
            output_path=output_path,
            csv_output_path=csv_output_path,
            cache_folder='cache',
            affiliation_conservative=affiliation_conservative,
            num_processes=num_processes,
            use_proxy=use_proxy,
            pin_colorful=pin_colorful,
            print_citing_affiliations=True
        )
        
        st.success(f"Citation map generated and saved to {output_path}.")
        
        # Read generated HTML map file and CSV
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as file:
                map_data = file.read()
            st.download_button("Download Citation Map", data=map_data, file_name="citation_map.html", mime="text/html")
        
        if os.path.exists(csv_output_path):
            with open(csv_output_path, 'r', encoding='utf-8') as file:
                csv_data = file.read()
            st.download_button("Download CSV", data=csv_data, file_name="citation_info.csv", mime="text/csv")
        
    else:
        st.error("Please enter a valid Google Scholar ID.")

# Place a button to clear the session and refresh
if st.button('Clear Session and Refresh'):
    clear_session()

# Optional: Clear the query parameter after page load to reset it
if 'refresh' in st.query_params:
    st.query_params.clear()

