import streamlit as st
import pandas as pd

folderName = "mai-shen-yun-main"

# Once user selects a month, use that month's data
month = st.pills("Month",["May","June","July","August","September","October"],default="October")
if month:
    data = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")

# Clean data

# Convert dollar amounts to float
data["Amount"] = (
    data["Amount"]
    .replace('[\$,]', '', regex=True)   # remove $ and ,
    .astype(float)                       # convert to float
)

option = st.selectbox('Select a category',["All products","Tea flavors","Meats","Fried Chicken"])
if(option == "Tea flavors"):
    # select only the items which refer to tea
    # use regex?
    data = data[data["Item Name"].str.contains(r"\Wtea", case=False, na=False)]
    
elif(option == "Meats"):
    # select only the items which refer to meat
    # use regex?
    dataT = data[data["Item Name"].str.contains(r"chicken", case=False, na=False)]
    chicken = dataT.sum()
    dataT = data[data["Item Name"].str.contains(r"beef", case=False, na=False)]
    beef = dataT.sum()
    dataT = data[data["Item Name"].str.contains(r"pork", case=False, na=False)]
    pork = dataT.sum()
    
    data = pd.DataFrame({"Item Name":["Chicken","Beef","Pork"],"Amount":[chicken[4],beef[4],pork[4]],"Count":[chicken[3],beef[3],pork[3]]})
    #DEBUG: st.write(data)
# TODO add chicken flavors
elif(option == "Fried Chicken"):
    data = data[data["Item Name"].str.contains(r"(fried chicken)|(crunch chicken)", case=False, na=False)]
    # chicken = dataT.sum()
    # data = pd.DataFrame({"Item Name":["Chicken","Beef","Pork"],"Amount":[chicken[4],beef[4],pork[4]],"Count":[chicken[3],beef[3],pork[3]]})

    
control = st.segmented_control('Display',["By Revenue","By Quantity"])
if(control == "By Revenue"):
    displayColumn = "Amount"
else:
    displayColumn = "Count"
st.bar_chart(data, x = "Item Name",y=displayColumn,horizontal=True)
#st.write(data)



