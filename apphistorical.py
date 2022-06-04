import streamlit as st
import pandas as pd
# for access to our data
import forETL as etl

def main():
    selected = "Historical Data"
    st.write("##")

    st.title(f"Previous Sales KPI's")
    st.write("Only Avg Spend Correct So Far")
    st.write("Should Actually Just Make This A Dropdown Under Main Instead")
    st.write("But Still Keep This For History Or Whatever Idk")
    st.write("##")

    # ---- for st.metric header widget ----
    col1, col2, col3 = st.columns(3)

    # grab historical avg spend per customer from db
    hist_avg_spend = etl.grab_all_cust_avg_spend_historical()

    # grab avg shop days by customer
    avg_shop_days = etl.grab_all_cust_avg_shop_days()
    
    # so should have a previous day table in db thats exactly the same but is basically cycling holding 2 things so can compare for delta
    # for now just do this for the new table 
    col1.metric(label="Avg Spend", value=f"${hist_avg_spend:.2f}", delta=None, delta_color="normal")
    col2.metric(label="Valued Customers", value=3, delta=0, delta_color="off")
    col3.metric(label="Avg Shop Days", value=f"{avg_shop_days:.1f}", delta=-1, delta_color="normal")
    
 

