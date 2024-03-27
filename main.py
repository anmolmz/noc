import streamlit as st
import pandas as pd

st.write('''
        # Find your career paths and respective NOC teer!
         ''')

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

tech = pd.read_csv('data/tech.csv', index_col = False)
acc = pd.read_csv('data/acc.csv', index_col = False)
markt = pd.read_csv('data/markt.csv', index_col = False)
hr = pd.read_csv('data/hr.csv', index_col = False)
hlsci = pd.read_csv('data/hlsci.csv', index_col = False)

if option == "Bachelor in Technology : Information Technology":
    st.markdown(tech.style.hide(axis="index").to_html(), unsafe_allow_html=True)

if option == "Bachelor of Business Administration: Marketing Management":
    st.markdown(markt.style.hide(axis="index").to_html(), unsafe_allow_html=True)

if option == "Bachelor of Business Administration: Human Resources Management":
    st.markdown(hr.style.hide(axis="index").to_html(), unsafe_allow_html=True)

if option == "Bachelor of Business Administration: Accounting":
    st.markdown(acc.style.hide(axis="index").to_html(), unsafe_allow_html=True)

if option == "Bachelor of Science in Health Sciences":
    st.markdown(hlsci.style.hide(axis="index").to_html(), unsafe_allow_html=True)

