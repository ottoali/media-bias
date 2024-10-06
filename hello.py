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
#hello.py


import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from datetime import datetime
pd.set_option("styler.render.max_elements", 1000)

ref = pd.read_csv("/Users/hamza/Library/Mobile Documents/iCloud~md~obsidian/Documents/Media Project/(use this)Final Refs Combined.csv")

lines_ = pd.read_csv("/Users/hamza/Library/Mobile Documents/iCloud~md~obsidian/Documents/Media Project/(use this)Final Lines Combined.csv")
df = lines_.copy()



####### things to add:

# 1. items per article
# 2. limit the database to july 31
# 3. DONE -- issue with NYT articles that are live and duplicates
# 4. remove wapo weird characters
# 5. remove "\n"
# 6. add button to remove all duplicates from a list (i.e. NYT lives where the line is repeated over multiple live articles/days)
# 7. decide how to show headlines
# 8. decide how to disallow downloads of all data
# 9. show data without showing articleID decide how to 
# 10. why are there so many duplicate headlines?
# 11. remove the ability of leaving | at the end of the text input

#########


# Title of the app
st.title("Media Analysis Database")

col1, col2 =st.columns([1, 1])

def highlight_search_term(text, term):
    if term and term.lower() in text.lower():
        start = text.lower().index(term.lower())
        end = start + len(term)
        return f"{text[:start]}∎∎∎{text[start:end]}∎∎∎{text[end:]}"
    return text


# Sample data

df['date'] = pd.to_datetime(df['Date'])

df = df.dropna()





# Text input for searching names
with col1:
    word_filter = st.text_input("Search for a term or phrase in a paragraph or line:")
    word_filter3 = st.text_input("Search for another mandatory term or phrase:")

    #selection of sources
    selected_sources= st.multiselect("Select sources to filter:", options=df['Source'].unique())

with col2:
    word_filter2 = st.text_input("Search for a second mandatory term in the paragraph/line:")
    
    start_date, end_date = st.slider(
    "Select Date Range:",
    min_value=df['date'].min().date(),
    max_value=df['date'].max().date(),
    value=(df['date'].min().date(), df['date'].max().date())
)


filtered_df = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]

term1 = ""
term2 = ""
term3 = ""



# Check if any options are selected
if selected_sources:
    # Filter the DataFrame based on selected options
    filtered_df = df[df['Source'].isin(selected_sources)]


    #if not empty search terms
    if word_filter!="" and len(word_filter)>2 and not word_filter.endswith("|"):
        filtered_df = filtered_df[filtered_df["body"].str.contains(word_filter, case=False)].sort_values(by="date",ascending=True)
        term1 = word_filter.replace("|"," OR ") 

        
        if word_filter2!="" and len(word_filter2)>2 and not word_filter2.endswith("|"):
           
            filtered_df = filtered_df[filtered_df["body"].str.contains(word_filter2, case=False)].sort_values(by="date",ascending=True)
            term2 = word_filter2.replace("|"," OR ") 
            
        

            if word_filter3!="" and len(word_filter3)>2 and not word_filter3.endswith("|"):

                filtered_df = filtered_df[filtered_df["body"].str.contains(word_filter3, case=False)].sort_values(by="date",ascending=True)
                term3 = word_filter3.replace("|"," OR ") 

        
        st.write("Searching for the following term(s) in the same paragraph:")
        st.write("  Query 1:", term1)
        if term2 !="":
            st.write("  Query 2:", term2)
        if term3 !="":
            st.write("  Query 3:", term3)

        st.markdown("---")  # This creates a horizontal line


        filtered_df['Highlighted'] = filtered_df['body'].apply(lambda x: highlight_search_term(x, word_filter))
        filtered_df = filtered_df[["Source","Date","Highlighted","Link","ArticleID","body","date"]]
        st.write(len(filtered_df)," Paragraphs containing terms(s)")
        st.write(filtered_df['ArticleID'].nunique()," Articles containing term(s)")   
        st.markdown("---")  # This creates a horizontal line
        
        st.write("This is a preview. For the full list, click on 'export' below.")   
        st.dataframe(filtered_df.head(100))
        
        
        csv = filtered_df.to_csv(index=False)  # Convert DataFrame to CSV format
        st.download_button(
            label="Export DataFrame as CSV",
            data=csv,
            file_name='news_data.csv',
            mime='text/csv')



        
        
        st.markdown("---")  # This creates a horizontal line
        grouped_df = filtered_df.groupby(['Source', 'date']).size().reset_index(name='Count')
        pivot_df = grouped_df.pivot(index='date', columns='Source', values='Count')

        pattern = "|".join(filtered_df["ArticleID"])
        headlines = ref[ref["ArticleID"].str.contains(pattern)]

        st.write("This is a list of all headlines in which the paragraphs above appear.")   
        st.dataframe(headlines)
        
        st.markdown("---")  # This creates a horizontal line
        st.write("This is a timeseries chart showing the presence of relevant paragraphs over time.")   
        st.bar_chart(pivot_df)




