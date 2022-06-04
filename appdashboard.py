# v1 dashboard app for some of our data
# ---- imports ----
# for web app
import streamlit as st
from streamlit_option_menu import option_menu
# for data manipulation and charts
import pandas as pd
# for multi page functionality
import appinsights as insgt
import appcharts as chrts
import apphistorical as hstrcl
# for access to our data
import forETL as etl


# ---- order and initialise our containers
top_bar = st.container()
pages = st.container()
home = st.container()


# nav menu
with top_bar:
    #---- as horizontal menu ----
    selected =  option_menu(
        menu_title=None, # required, can be text or None
        options=["Home", "Insights", "Charts", "Historical"], # required
        icons=["house-door", "magic", "graph-up-arrow", "watch"], # optional
        menu_icon="ui-checks", # optional
        default_index=0, # optional
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#F0E3CA"},
            "icon": {"color": "#15133C", "font-size": "20px"},
            "nav-link": {"color": "#1B1A17", "font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#C0B5A1"},
            "nav-link-selected": {"background-color": "#FF8303", "font-weight": "700"},
        }
    ) # clock, search, watch


with pages:
    if selected == "Home":
        with home:
            st.write("##")

            st.title(f"Sales KPI Dashboard")
            st.write("##")

            # ---- for st.metric header widget ----
            col1, col2, col3 = st.columns(3)

            # grab current & historical avg spend per customer from db
            avg_spend = etl.grab_all_cust_avg_spend_proper()
            hist_avg_spend = etl.grab_all_cust_avg_spend_historical()
            # calculate the difference for the delta
            avg_spend_delta = avg_spend - hist_avg_spend
            avg_spend_delta = f"{avg_spend_delta:.2f}"
            avg_spend_delta = float(avg_spend_delta)

            # grab avg shop days per customer
            avg_shop_days = etl.grab_all_cust_avg_shop_days()
            
    	    # so should have a previous day table in db thats exactly the same but is basically cycling holding 2 things so can compare for delta
            # for now just do this for the new table 
            col1.metric(label="Avg Spend", value=f"${avg_spend:.2f}", delta=avg_spend_delta, delta_color="normal")
            col2.metric(label="Valued Customers", value=3, delta=0, delta_color="off")
            col3.metric(label="Avg Shop Days", value=f"{avg_shop_days:.1f}", delta=-1, delta_color="normal")

            st.write("---")
            st.write("##")
            st.write(""" #### Amount Of Items Sold By Price """)
            dashboard_data = pd.read_csv("CustomerSalesData.csv")
            dash_chart = pd.DataFrame(dashboard_data["purchase_amount"].value_counts()).head(31)
            st.bar_chart(dash_chart)

            st.write("---")
            st.write("##")
            nav_location = f'<p style="font-size: 12px;">{selected}</p>'
            st.markdown(nav_location, unsafe_allow_html=True)

    # insights page
    if selected == "Insights":
        insgt.main()

    # charts page
    if selected == "Charts":
        chrts.main()

    # historical page
    if selected == "Historical":
        hstrcl.main()



# ---- styling for fonts ----
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');

			html, body [class*="css"]  {
			font-family: Roboto, sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)


# padd = 50
# container_style = f"""
# 			<style>
#             .css-1n76uvr.e1tzin5v0
            
#             {{
#             padding-top: {padd}px;
#             padding-right: {padd}px;
#             padding-left: {padd}px;
#             padding-bottom: 100px;
#             }}
#             </style>
# 			"""
# st.markdown(container_style, unsafe_allow_html=True)