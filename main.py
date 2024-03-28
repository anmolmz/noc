import streamlit as st
import pandas as pd
from selenium import webdriver
import sys

st.write('''
        # Find your career paths and respective NOC teer!
         ''')

# Drop down for degree options
option = st.selectbox(
   "Which program are you enrolled in at KPU?",
   ("Bachelor in Technology : Information Technology", 
    "Bachelor of Business Administration: Marketing Management", 
    "Bachelor of Business Administration: Human Resources Management",
    "Bachelor of Business Administration: Accounting",
    "Bachelor of Science in Health Sciences"),
   index=None,
   placeholder="Select your degree...",
)

# Creating dataframes for each degree
tech = pd.read_csv('data/tech.csv', index_col = False)
acc = pd.read_csv('data/acc.csv', index_col = False)
markt = pd.read_csv('data/markt.csv', index_col = False)
hr = pd.read_csv('data/hr.csv', index_col = False)
hlsci = pd.read_csv('data/hlsci.csv', index_col = False)

# Dictionary mapping option to dataframes
option_df_dict = {
    "Bachelor in Technology : Information Technology": tech,
    "Bachelor of Business Administration: Marketing Management": markt,
    "Bachelor of Business Administration: Human Resources Management": hr,
    "Bachelor of Business Administration: Accounting": acc,
    "Bachelor of Science in Health Sciences": hlsci
}

# Initiating empty dataframe
df = pd.DataFrame()

# Get the DataFrame based on 'option'(degree) selected by user from drop down menu
df = option_df_dict.get(option, df) # defaults to empty dataframe until option is selected

# Display the information when option is selected
# Before that create an empty string to store the HTML content because if I render each row individually, header will appear each time
html_content = ""
if option != None:
    for index, row in df.iterrows():
        
        # Generate the indeed URL with query string based on job title
        query = '?q=' + row['JOB CATEGORY'].replace(' ', '+') # vjk parameter is populated by indeed itself based on first job in listing
        url = f"https://ca.indeed.com/jobs{query}"
        
        # Create indeed hyperlink for the row
        hyperlink_text = 'Try it!'
        hyperlink =  f"<a href='{url}'>{hyperlink_text}</a>"

        # Add the row's HTML content with hyperlink to the overall HTML content
        html_content += f"<tr><td>{row['JOB CATEGORY']}</td><td>{row['NOC TEER']}</td><td>{hyperlink}</td></tr>"
    
    # Concatenate the HTML content for the table
    html_table = f"<table><tr><th>JOB CATEGORY</th><th>NOC TEER</th><th>Search Job</th></tr>{html_content}</table>"

    # Display the HTML table
    st.markdown(html_table, unsafe_allow_html=True) 
    # **************Rendering this HTML in st is not good for security against XSS. We'll show it as a QA's concern however in our case we're not taking any input and our even our CSV files are not hosted on a public server but in actual production scenario an attack is possibile **************
    
    
