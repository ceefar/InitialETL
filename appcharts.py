import streamlit as st
import pandas as pd

def main():
    selected = "Data"

    st.write("##")
    st.title(f"Sales Data")
    


    st.write("##")
    st.write(""" ### The DB Sales Data """)
    st.write("Cleaned and updated from original dataset")
    
    def text_highlighter(input_text:str = "highlighted", webcolor="#0083b8"):
        highlighted = f'<span style="color:{webcolor};">{input_text}</span>'
        return highlighted
    
    st.markdown(f"* *fields {text_highlighter('highlighted blue')} have been cleaned*", unsafe_allow_html=True)
    st.markdown(f"* *fields {text_highlighter('highlighted green', 'green')} have been updated from product_id data*", unsafe_allow_html=True)
    st.write("##")

    def style_specific_cell(x):
        color = 'background-color:#0083b8'
        color2 = 'background-color:green'
        df1 = pd.DataFrame('', index=x.index, columns=x.columns)
        df1.iloc[2, 1] = color
        df1.iloc[5, 2] = color2
        df1.iloc[24, 3] = color
        df1.iloc[26, 2] = color
        return df1

    dashboard_data = pd.read_csv("CustomerSalesData.csv")
    st.dataframe(dashboard_data.style.apply(style_specific_cell, axis=None))

    st.write("---")

    st.write("##")
    st.write(""" ### The Original DataSet """)
    st.markdown(f"* *missing fields have been {text_highlighter('highlighted red', '#ff3632')}*", unsafe_allow_html=True)
    original_data = pd.read_csv("sales_data.csv")
    st.dataframe(original_data.head(31).style.highlight_null(null_color='#ff3632')) #
    st.write("---")
    st.write("##")
    nav_location = f'<p style="font-size: 12px;">{selected}</p>'
    st.markdown(nav_location, unsafe_allow_html=True) 

    

