import streamlit as st
import pandas as pd

st.write("Hello world")

data = pd.read_csv("data/August_Data_Matrix.csv")
st.write(data)