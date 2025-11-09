import streamlit as st
import pandas as pd
import altair as alt

folderName = "mai-shen-yun-main"

# Once user selects a month, use that month's data
month = st.pills("Month",["May","June","July","August","September","October"],default="October")
if not month:
    month = "October"
data = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")

st.subheader(f"Popularity by Category for {month}")
# Create two columns
col1, col2 = st.columns([1, 1.5])  # Adjust width ratio (table:chart)
# Clean data

# Convert dollar amounts to float
data["Amount"] = (
    data["Amount"]
    .replace('[\$,]', '', regex=True)   # remove $ and ,
    .astype(float)                       # convert to float
)

option = st.selectbox('Select a category',["All products","Tea flavors","Meats","Fried Chicken"])
if(option == "Tea flavors"):
    # Select only the items to display which refer to tea using regex
    data = data[data["Item Name"].str.contains(r"\Wtea", case=False, na=False)]
    
elif(option == "Meats"):
    # Select only the items which refer to meat
    dataT = data[data["Item Name"].str.contains(r"chicken", case=False, na=False)]
    chicken = dataT.sum()
    dataT = data[data["Item Name"].str.contains(r"beef", case=False, na=False)]
    beef = dataT.sum()
    dataT = data[data["Item Name"].str.contains(r"pork", case=False, na=False)]
    pork = dataT.sum()
    
    data = pd.DataFrame({"Item Name":["Chicken","Beef","Pork"],"Amount":[chicken[4],beef[4],pork[4]],"Count":[chicken[3],beef[3],pork[3]]})
elif(option == "Fried Chicken"):
    # Select fried chicken data values
    data = data[data["Item Name"].str.contains(r"(fried chicken)|(crunch chicken)", case=False, na=False)]

    
control = st.segmented_control('Display',["By Revenue","By Quantity"])
if(control == "By Revenue"):
    # Display by dollar value
    displayColumn = "Amount"
else:
    # Display by quantity
    displayColumn = "Count"

#st.bar_chart(data, x = "Item Name",y=displayColumn,horizontal=True)

# Create two columns for side-by-side layout
col1, col2 = st.columns([1.8, 1])  # Adjust ratio for layout



with col1:
    data = data.sort_values(by=displayColumn).reset_index(drop=True)
    st.bar_chart(data, x="Item Name", y=displayColumn, horizontal=True,sort=f"-{displayColumn}")
#     chart = (
#     alt.Chart(data)
#     .mark_bar()
#     .encode(
#         x=alt.X(displayColumn, title=control),
#         y=alt.Y("Item Name", sort="-x", title=None),  # <- ensures sorted by x (displayColumn)
#         tooltip=["Item Name", "Amount", "Count"]
#     )
#     .properties(height=400)
# )

# st.altair_chart(chart, use_container_width=True)
with col2:
    st.markdown("### Summary of category")
    total_amount = data["Amount"].sum()
    total_count = data["Count"].sum()
    # most_popular_row = data.loc[data["Count"].idxmax()]
    # most_popular = most_popular_row["Item Name"]

    st.metric("Total Revenue This Month", f"${total_amount:,.2f}")
    st.metric("Total Quantity Sold", int(total_count))
    #st.metric(f"Most popular of {option}",most_popular)
    top5 = data.sort_values(by="Count", ascending=False).head(5)
    st.write("### 🏆 Top 5 Most Popular Items")
    st.dataframe(top5["Item Name"])

# # Define a rainbow color sequence
# rainbow_colors = [
#     '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#EE82EE'
# ]

# # Create Altair chart with custom color scale
# chart = alt.Chart(data).mark_bar().encode(
#     x='Item Name', # TODO what
#     y=displayColumn,
#     color=alt.Color('Category:N', scale=alt.Scale(range=rainbow_colors), legend=None)
# )

# st.altair_chart(chart)

