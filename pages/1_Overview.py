import streamlit as st
import pandas as pd

def render_overview():
    st.header("Overview Page")
    st.write("This is where the Overview metrics will go.")
    
    # Example: load data (replace with actual CSV path)
    # df = pd.read_csv("data/october_items.csv")
    # st.dataframe(df.head())
