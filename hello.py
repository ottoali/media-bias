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
CSV_FILES = ["lines_output_part_1.csv","lines_output_part_2.csv","lines_output_part_3.csv","lines_output_part_4.csv",
             "lines_output_part_5.csv","lines_output_part_6.csv","lines_output_part_7.csv","lines_output_part_8.csv",
            "lines_output_part_9.csv","lines_output_part_10.csv"]  # List of CSV files

ref_file = ["(use this)Final Refs Combined.csv"]
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

df = load_data_from_github(CSV_FILES)

ref = load_data_from_github(ref_file)




def screen_one():

    # Sample data
    
    
    # Title of the app
    st.title("Dynamic Table")

    # Dropdown for selecting a city
    #date_filter = st.selectbox("Select a date:", options=["All"] + df["Date"].unique().tolist())

    df['date'] = pd.to_datetime(df['Date'])

    df = df.dropna()

    start_date, end_date = st.slider(
        "Select Date Range:",
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date(),
        value=(df['date'].min().date(), df['date'].max().date())
    )

    filtered_df = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]




    # Text input for searching names
    with col1:
        word_filter = st.text_input("Search for a word:")

    with col2:
        word_filter2 = st.text_input("Search for a word2:")



    #selection of sources
    selected_sources= st.multiselect("Select sources to filter:", options=df['Source'].unique())

    # Check if any options are selected
    if selected_sources:
        # Filter the DataFrame based on selected options
        filtered_df = df[df['Source'].isin(selected_sources)]
        
        #if not empty search terms
        if word_filter!="":
            if len(word_filter)>2:

                if word_filter:
                    filtered_df = filtered_df[filtered_df["body"].str.contains(word_filter, case=False)].sort_values(by="date",ascending=True)
                    filtered_df = filtered_df[filtered_df["body"].str.contains(word_filter2, case=False)].sort_values(by="date",ascending=True)

                    st.write(len(filtered_df)," Paragraphs containing term")
                    st.write(filtered_df['ArticleID'].nunique()," Articles containing term")
                    st.dataframe(filtered_df.head(2000))
                    
                    csv = filtered_df.to_csv(index=False)  # Convert DataFrame to CSV format
                    st.download_button(
                        label="Export DataFrame as CSV",
                        data=csv,
                        file_name='news_data.csv',
                        mime='text/csv'
                    )

                    grouped_df = filtered_df.groupby(['Source', 'date']).size().reset_index(name='Count')
                    pivot_df = grouped_df.pivot(index='date', columns='Source', values='Count')


                    pattern = "|".join(filtered_df["ArticleID"])
                    headlines = ref[ref["ArticleID"].str.contains(pattern)]
                    st.dataframe(headlines)

                    st.bar_chart(pivot_df)


                else:
                    st.write("enter search term.")
            else:
                st.write("enter search term.")



    else:
        st.write("Please select at least one fruit to view results.")



    # Display the DataFrame with custom CSS class

    #st.dataframe(filtered_df.style.set_table_attributes('class="wrapped-table"'))
        


    st.markdown(
        """
        <style>
        .wrapped-table td {
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 200px;  /* Adjust width as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def screen_two():
    
    st.write("Please select at least one fruit to view results.")




col1, col2 =st.columns([1,1])


st.sidebar.title("Navigation")

# Create radio buttons for navigation
screen = st.sidebar.radio("Select a filter:", ("Article Body", "Article Headline"))


# Display the selected screen
if screen == "Article Body":
    screen_one()
else:
    screen_two()
