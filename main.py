import streamlit as st
import pandas as pd
import requests
import ipinfo
from dotenv import load_dotenv
import os

# Load variables from the .env file into the environment
load_dotenv()

# Access the environment variables
access_token = os.getenv("ACCESS_TOKEN")

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
df = option_df_dict.get(option, df) # defaults to empty dataframe until option is selected and we have the key in dictionary

# Retreiving the IP address of user and then location data from IP add. using two APIs ipify and ipinfo
def get_ip(): 
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location(): 
    ip_address = get_ip()
    access_token = access_token # This access token is issued on my personal email, max. 50,000 reqs/month
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)
    city = details.city
    return city

city = get_location()
 
# creating location query to be used for indeed search
if city != None:
    loc_query = '&l=' + str(city)
else:
    loc_query = '&l=British+Columbia'

# Display the information when option is selected
# Before that create an empty string to store the HTML content because if each row is rendered individually, header and index will appear each time
html_content = ""
if option != None: # This is default until option is selected by user
    for index, row in df.iterrows():
        
        # Generate the indeed URL with query string based on job title and location
        # vjk parameter is populated by indeed itself based on first job in listing
        job_query = '?q=' + row['JOB CATEGORY'].replace(' ', '+') 
        query = job_query + loc_query
        url = f"https://ca.indeed.com/jobs{query}"
        
        # Create indeed hyperlink for the row
        hyperlink_text = "Job Search"
        hyperlink =  f"<a style='text-decoration: none;' href='{url}'>{hyperlink_text}</a>"

        # Add the row's HTML content with hyperlink and tooltip to the overall HTML content
        # TODO: using br tag to organize a little but there should be some better way
        html_content += f"<tr><td>{row['JOB CATEGORY']}<br><span title='{row['DESCRIPTION']}'><i>Description</i></span><br>{hyperlink}</td><td>{row['NOC TEER']}</td></tr>"
    
    # Concatenate the HTML content for the table
    html_table = f"<table><tr><th>JOB CATEGORY</th><th>NOC TEER</th></tr>{html_content}</table>"

    # Display the HTML table
    st.markdown(html_table, unsafe_allow_html=True) 
    # **************Rendering this HTML in st is not good for security against XSS. We'll show it as a QA's concern however in our case we're not taking any input and our even our CSV files are not hosted on a public server but in actual production scenario an attack is possibile **************

