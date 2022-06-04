import streamlit as st
import pandas as pd

def main():
    selected = "Charts"

    st.write("##")
    st.title(f"Sales Charts")
    
    st.write("---")
    st.write("##")
    st.write(""" #### The DB Sales Data """)
    dashboard_data = pd.read_csv("CustomerSalesData.csv")
    st.write(dashboard_data.head(31))

    st.write("##")
    st.write(""" #### The Original DataSet """)
    original_data = pd.read_csv("sales_data.csv")
    st.write(original_data.head())

    st.write("---")
    st.write("##")
    nav_location = f'<p style="font-size: 12px;">{selected}</p>'
    st.markdown(nav_location, unsafe_allow_html=True) 

    

