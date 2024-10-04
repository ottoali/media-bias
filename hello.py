#hello.py


import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from datetime import datetime
pd.set_option("styler.render.max_elements", 1000)

ref = pd.read_csv("https://raw.githubusercontent.com/ottoali/media-bias/refs/heads/main/wwmissing.csv")

lines_ = pd.read_csv("https://raw.githubusercontent.com/ottoali/media-bias/refs/heads/main/wwmissing.csv")

st.dataframe(lines_)

word_filter2 = st.text_input("Search for a word2:")

