import streamlit as st
import pandas as pd
import os
import chat

suggested_questions = [
    "Which ingredients were understocked this month?",
    "Which ingredients were overstocked this month?"
]

with st.sidebar:
    st.header("Noodlebot")
    st.write("**Suggested Questions:**")
    for question in suggested_questions:
        if st.button(question):
            user_input = question
            response = chat.get_chat_response(user_input)
            st.markdown(f"**Q:** {question}")
            st.markdown(f"**A:** {response}")

    # Also keep a text input for custom questions
    user_input = st.text_input("Ask a question:")
    if user_input:
        response = chat.get_chat_response(user_input)
        st.markdown(f"**Q:** {user_input}")
        st.markdown(f"**A:** {response}")

# st.write("Displaying by quantity sold")
# pressed = st.button("Display by revenue generated") # TODO


st.set_page_config(layout="wide")



#read csv
folderName = "mai-shen-yun-main"

# #defines a default bc otherwise month would be undefined
# month = "October"
# monthData = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")
col1, col2 = st.columns([3, 2])  # adjust width ratio as you like

with col1:
    st.title("Inventory")

with col2:
    month = st.pills("Month",["May","June","July","August","September","October"],default="October")

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



# -----------------------------
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
            qty *= 453  # convert to grams
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

calculated_usage["Usage"] = calculated_usage["Usage"].round(0).astype(int)
calculated_usage["Shipment"] = calculated_usage["Shipment"].round(0).astype(int)

calculated_usage["Difference"] = (calculated_usage["Shipment"] - calculated_usage["Usage"]).round(0).astype(int)
#display_df = calculated_usage[["Ingredient", "Usage", "Shipment", "Difference"]].reset_index(drop=True)
display_df = calculated_usage[["Ingredient", "Usage", "Shipment"]].reset_index(drop=True)

# -----------------------------
# FILTER OPTIONS
# -----------------------------
option = st.selectbox(
    "Select a category",
    ["All products", "Overstocked", "Understocked"]
)

if option == "Overstocked":
    filtered_df = display_df[display_df["Shipment"] > display_df["Usage"]]
elif option == "Understocked":
    filtered_df = display_df[display_df["Shipment"] < display_df["Usage"]]
else:
    filtered_df = display_df

# -----------------------------
# DISPLAY TABLE + CHART
# -----------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Ingredient Usage ({option}) - {month}")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader(f"Ingredient Comparison ({option})")

    df_melted = filtered_df.melt(
        id_vars=["Ingredient"],
        value_vars=["Usage", "Shipment"],
        var_name="Type",
        value_name="Amount"
    )

    chart = (
        alt.Chart(df_melted)
        .mark_bar()
        .encode(
            x=alt.X("Ingredient:N", sort=None),
            y="Amount:Q",
            color="Type:N",
            xOffset="Type:N",
            tooltip=["Ingredient", "Type", "Amount"]
        )
        .properties(width=800)
    )
    st.altair_chart(chart, use_container_width=True)


# -----------------------------
# Summary box: top 5 over/under stocked
# -----------------------------
st.subheader("Inventory Summary")

top_overstocked = calculated_usage.sort_values(by="Difference", ascending=False).head(5)
top_understocked = calculated_usage.sort_values(by="Difference", ascending=True).head(5)

st.write("**Top 5 Overstocked Ingredients (Shipment >> Usage):**")
st.table(top_overstocked[["Shipment", "Usage", "Difference"]])

st.write("**Top 5 Understocked Ingredients (Usage >> Shipment):**")
st.table(top_understocked[["Shipment", "Usage", "Difference"]])