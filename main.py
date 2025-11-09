import streamlit as st
import pandas as pd

st.write("Displaying by quantity sold")
pressed = st.button("Display by revenue generated") # TODO

# TODO: clean data
folderName = "mai-shen-yun-main"
month = "August"
data = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")

# Clean data

# Convert dollar amounts to float
data["Amount"] = (
    data["Amount"]
    .replace('[\$,]', '', regex=True)   # remove $ and ,
    .astype(float)                       # convert to float
)

# TODO finish adding categories
# TODO implement bar chart by category
# TODO implement filter selector thing on the right
st.pills("Month",["May","June","July","August","September","October"])
option = st.selectbox('Select a category',["All categories","Boba flavors","Meats"])
if(option == "Boba flavors"):
    data = data[data['']]

# TODO make sure to clean the count column - if there's a comma in the value it becomes a string, but all of that category should be ints!
control = st.segmented_control('Display',["By Revenue","By Quantity"])
if(control == "By Revenue"):
    displayColumn = "Amount"
else:
    displayColumn = "Count"
st.bar_chart(data, x = "Item Name",y=displayColumn,horizontal=True)
#st.write(data)

