import streamlit as st
import pandas as pd
import os

# st.write("Displaying by quantity sold")
# pressed = st.button("Display by revenue generated") # TODO

st.title("Inventory")
st.set_page_config(layout="wide")

#read csv
folderName = "mai-shen-yun-main"

# #defines a default bc otherwise month would be undefined
# month = "October"
# monthData = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")


month = st.pills("Month",["May","June","July","August","September","October"], default = "October")
if not month:
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

# # Sort totals descending
# total_sorted = total_ingredient_usage.T.sort_values(by=0, ascending=False)
# total_sorted.columns = ["Total Used"]

# st.subheader(f"Total Ingredient Usage for {month}")

# # Create two columns
# col1, col2 = st.columns([1, 1.5])  # Adjust width ratio (table:chart)

# # Left column → table
# with col1:
#     st.dataframe(total_sorted, use_container_width=True)

# # Right column → chart
# with col2:
#     st.subheader("Top 10 Ingredients")
#     st.bar_chart(total_sorted.head(10))
import altair as alt
shipments = pd.read_csv(f"{folderName}/MSY Data - Shipment.csv")

# -----------------------------
# Calculate monthly shipments
# -----------------------------
freq_map = {"weekly": 4, "biweekly": 2, "monthly": 1}

shipment_totals = {}
for ing in total_ingredient_usage.columns:
    ing_lower = ing.lower()
    matched = None
    for _, row in shipments.iterrows():
        ship_ing_lower = row["Ingredient"].strip().lower()
        if ship_ing_lower in ing_lower:
            matched = row
            break
    if matched is not None:
        qty = matched["Quantity per shipment"]
        unit = matched["Unit of shipment"].lower()
        num_shipments = matched["Number of shipments"]
        freq = matched["frequency"].lower()
        if unit == "lbs":
            qty *= 453.592  # convert to grams
        total_per_month = qty * num_shipments * freq_map.get(freq, 1)
        shipment_totals[ing] = total_per_month
    else:
        shipment_totals[ing] = 0

# -----------------------------
# Prepare DataFrame for display
# -----------------------------
calculated_usage = total_ingredient_usage.T.rename(columns={0: "Usage"})
calculated_usage["Ingredient"] = calculated_usage.index
calculated_usage["Shipment"] = calculated_usage["Ingredient"].apply(lambda x: shipment_totals.get(x, 0))

# Remove old index for cleaner display
display_df = calculated_usage[["Ingredient", "Usage", "Shipment"]].reset_index(drop=True)

# -----------------------------
# Display in two columns: table + bar chart
# -----------------------------
col1, col2 = st.columns([1,2])

with col1:
    st.subheader(f"Total Ingredient Usage - {month}")
    st.dataframe(display_df)

with col2:
    st.subheader("Top Ingredients Comparison")
    # Melt for grouped bar chart
    df_melted = display_df.melt(id_vars=["Ingredient"], value_vars=["Usage", "Shipment"],
                                var_name="Type", value_name="Amount")
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('Ingredient:N', sort=None),
        y='Amount:Q',
        color='Type:N',
        xOffset='Type:N',
        tooltip=['Ingredient','Type','Amount']
    ).properties(width=800)
    st.altair_chart(chart, use_container_width=True)