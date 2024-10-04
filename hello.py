#hello.py


import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from datetime import datetime
pd.set_option("styler.render.max_elements", 1000)

ref = pd.read_csv("https://raw.githubusercontent.com/ottoali/media-bias/refs/heads/main/wwmissing.csv")

lines_ = pd.read_csv("https://raw.githubusercontent.com/ottoali/media-bias/refs/heads/main/wwmissing.csv")


####### things to add:
'''
1. items per article
2. limit the database to july 31
3. DONE -- issue with NYT articles that are live and duplicates
4. remove wapo weird characters
5. remove "\n"
6. add button to remove all duplicates from a list (i.e. NYT lives where the line is repeated over multiple live articles/days)
7. decide how to show headlines
8. decide how to disallow downloads of all data
9. show data without showing articleID decide how to 


'''
#########



def screen_one():

    # Sample data
    df = lines_.copy()

    #filtered_df = df.copy()

    # Title of the app
    st.title("Dynamic Table Example")

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
