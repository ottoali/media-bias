#hello.py

import requests
import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from datetime import datetime
pd.set_option("styler.render.max_elements", 1000)

GITHUB_USERNAME = "ottoali"  # Replace with your GitHub username
REPO_NAME = "data"              # Replace with your repo name
FILE_PATH = "(use this)Final Refs Combined.csv"  # Replace with the path to your CSV file
GITHUB_TOKEN = st.secrets["key"]  # Store your token in Streamlit secrets


# Function to fetch CSV from GitHub
def load_data_from_github():
    url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{FILE_PATH}"
    
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

# Streamlit app
st.title("Secure CSV Data from GitHub")

# Load the data
data = load_data_from_github()

# Display the DataFrame if loaded successfully
if data is not None:
    st.write("Data from the CSV:")
    st.dataframe(data)


