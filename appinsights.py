import streamlit as st
import pandas as pd

def main():
    selected = "Insights"

    st.write("##")
    st.title(f"Customer Insights")

    st.write("##")
    st.write(""" #### The Insights Data """)
    insights_data = pd.read_csv("CustomerSpendingInsights.csv")
    st.write(insights_data.head())

    st.write("---")
    st.write("##")

    insgt_chart = pd.DataFrame(insights_data["total_spend"]).head()
    st.bar_chart(insgt_chart)
    
    st.write("---")
    st.write("##")
    nav_location = f'<p style="font-size: 12px;">{selected}</p>'
    st.markdown(nav_location, unsafe_allow_html=True) 



    