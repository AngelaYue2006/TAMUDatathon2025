import streamlit as st
import pandas as pd
import os

# st.write("Displaying by quantity sold")
# pressed = st.button("Display by revenue generated") # TODO

st.title("something")
st.set_page_config(layout="wide")

#read csv
folderName = "mai-shen-yun-main"

# #defines a default bc otherwise month would be undefined
# month = "October"
# monthData = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")


month = st.pills("Month",["May","June","July","August","September","October"], default = "October")
monthData = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")

ingredientsData = pd.read_csv(f"{folderName}/MSY Data - Ingredient.csv")

#Create a DataFrame to store total ingredient usage
#pd.DataFrame creates new dataframe
#0 initializes with 0
#index=[0] creates a single row dataframe
#columns = ingredientsData.columns[1:] uses all columns except "Item name"
total_ingredient_usage = pd.DataFrame(0, index=[0], columns=ingredientsData.columns[1:])
#the columns after "Item name" represent ingredient amounts

#loop through each menu item in the ingredients dataset
for _, row in ingredientsData.iterrows():
    item_name = str(row["Item name"]).lower()

    #find all rows in monthData whose Item Name contains this item name (partial match)
    matched_rows = monthData[monthData["Item Name"].str.lower().str.contains(item_name, na=False)]

    if not matched_rows.empty:
        #compute total count of a certain ingredient used in the month
        total_count = matched_rows["Count"].sum()

        #multiply each ingredient quantity by the total count
        for ingredient in ingredientsData.columns[1:]:
            if pd.notna(row[ingredient]):  #skip NaNs
                total_ingredient_usage.at[0, ingredient] += row[ingredient] * total_count

# #Display the total ingredient usage for the month
# print("=== Total Ingredient Usage for", month, "===")
# print(total_ingredient_usage.T.sort_values(by=0, ascending=False))


# Sort totals descending
total_sorted = total_ingredient_usage.T.sort_values(by=0, ascending=False)
total_sorted.columns = ["Total Used"]

st.subheader(f"Total Ingredient Usage for {month}")

# Create two columns
col1, col2 = st.columns([1, 1.5])  # Adjust width ratio (table:chart)

# Left column → table
with col1:
    st.dataframe(total_sorted, use_container_width=True)

# Right column → chart
with col2:
    st.subheader("Top 10 Ingredients")
    st.bar_chart(total_sorted.head(10))