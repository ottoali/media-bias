#hello.py

import requests
from io import StringIO
import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from datetime import datetime
pd.set_option("styler.render.max_elements", 1000)

GITHUB_USERNAME = "ottoali"  # Replace with your GitHub username
REPO_NAME = "data"              # Replace with your repo name
CSV_FILES = ["lines_output_part_1","lines_output_part_2","lines_output_part_3","lines_output_part_4",
             "lines_output_part_5","lines_output_part_6","lines_output_part_7","lines_output_part_8",
            "lines_output_part_9","lines_output_part_10","lines_output_part_11"]  # List of CSV files

             
GITHUB_TOKEN = st.secrets["key"]  # Access token from Streamlit secrets

# Function to fetch and combine CSVs from GitHub
def load_data_from_github(file_list):
    combined_data = pd.DataFrame()  # Initialize an empty DataFrame

    for file_name in file_list:
        url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{file_name}"
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            csv_data = pd.read_csv(StringIO(response.text))
            combined_data = pd.concat([combined_data, csv_data], ignore_index=True)  # Combine DataFrames
        else:
            st.error(f"Failed to load data from {file_name}.")
    
    return combined_data
    
data = load_data_from_github(CSV_FILES)

# Display the DataFrame if loaded successfully
if not data.empty:
    st.write("Combined Data from CSVs:")
    st.dataframe(data)
else:
    st.warning("No data loaded.")

