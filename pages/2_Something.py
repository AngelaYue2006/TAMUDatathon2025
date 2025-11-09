import streamlit as st
import pandas as pd
import os

# st.write("Displaying by quantity sold")
# pressed = st.button("Display by revenue generated") # TODO

st.title("something")

#read csv
folderName = "mai-shen-yun-main"
month = "October"
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

# --- Streamlit display section ---
st.subheader(f"Total Ingredient Usage for {month}")
st.dataframe(total_sorted)

# Optionally, visualize top 10 ingredients
st.subheader("Top 10 Ingredients by Quantity Used")
st.bar_chart(total_sorted.head(10))