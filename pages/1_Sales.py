import streamlit as st
import pandas as pd
import altair as alt
import chat

st.set_page_config(layout="wide")

suggested_questions = [
    "What are the most popular items?",
    "Any trends in ingredient usage?"
]

with st.sidebar:
    st.header("Noodlebot")
    st.write("**Suggested Questions:**")
    for question in suggested_questions:
        if st.button(question):
            user_input = question
            with st.spinner("Thinking..."):
                response = chat.get_chat_response(user_input)
            st.markdown(f"**Q:** {question}")
            st.markdown(f"**A:** {response}")

    # Also keep a text input for custom questions
    user_input = st.text_input("Ask a question:")
    if user_input:
        with st.spinner("Thinking..."):
            response = chat.get_chat_response(user_input)
        st.markdown(f"**Q:** {user_input}")
        st.markdown(f"**A:** {response}")

folderName = "data"
# Create two columns: one for title, one for pills
col1, col2 = st.columns([3, 2])  # adjust width ratio as you like

with col1:
    st.title("Overview")

with col2:
    month = st.pills("Month",["May","June","July","August","September","October"],default="October")

if not month:
    month = "October"
data = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")



# # Once user selects a month, use that month's data
# month = st.pills("Month",["May","June","July","August","September","October"],default="October")
# if not month:
#     month = "October"
# data = pd.read_csv(f"{folderName}/{month}/{month}_Data_Items.csv")

st.subheader(f"Popularity by Category - {month}")
# Create two columns
col1, col2 = st.columns([1, 1.5])  # Adjust width ratio (table:chart)
# Clean data

# Convert dollar amounts to float
data["Amount"] = (
    data["Amount"]
    .replace('[\$,]', '', regex=True)   # remove $ and ,
    .astype(float)                       # convert to float
)

# TODO add dessert category
# TODO add bowl? category to aummarize what kind of bowl is more popular
# appetizers
# drinks category
option = st.selectbox('Select a category',["All products","Meats","Fried Chicken","Bowls","Tea flavors","Dessert"])
if option == "Tea flavors":
    # Select only the items to display which refer to tea using regex
    data = data[data["Item Name"].str.contains(r"\Wtea", case=False, na=False)]
    
elif option == "Meats":
    # Select only the items which refer to meat
    dataT = data[data["Item Name"].str.contains(r"chicken", case=False, na=False)]
    chicken = dataT.sum()
    dataT = data[data["Item Name"].str.contains(r"beef", case=False, na=False)]
    beef = dataT.sum()
    dataT = data[data["Item Name"].str.contains(r"pork", case=False, na=False)]
    pork = dataT.sum()
    
    data = pd.DataFrame({"Item Name":["Chicken","Beef","Pork"],"Amount":[chicken[4],beef[4],pork[4]],"Count":[chicken[3],beef[3],pork[3]]})
elif option == "Fried Chicken":
    # Select fried chicken data values
    data = data[data["Item Name"].str.contains(r"(fried chicken)|(crunch chicken)", case=False, na=False)]
elif option == "Bowls":
    # Select only the items which refer to bowls
    data = data[data["Item Name"].str.contains(r"(rice noodle)|(ramen)|(soup)", case=False, na=False)]
    
    #commented out code was organizing by type of bowl
    # # Select tossed rice noodle
    # dataT = data[data["Item Name"].str.contains(r"Tossed rice noodle", case=False, na=False)]
    # tossedRiceNoodle = dataT.sum()
    
    # # Select tossed ramen
    # dataT = data[data["Item Name"].str.contains(r"Tossed ramen", case=False, na=False)]
    # tossedRamen = dataT.sum()
    
    # # Select ramen (untossed)
    # dataT = data[data["Item Name"].str.contains(r"(?<!tossed )ramen", case=False, na=False)]
    # ramen = dataT.sum()
    
    # data = pd.DataFrame({"Item Name":["Tossed Rice Noodles","Tossed Ramen","Ramen"],
    #                      "Amount":[tossedRiceNoodle[4],tossedRamen[4],ramen[4]],
    #                      "Count":[tossedRiceNoodle[3],tossedRamen[3],ramen[3]]})
elif option == "Dessert":
    
    #select desserts
    data = data[data["Item Name"].str.contains(r"(Brown Sugar Rice Cake)|(Bingsu)", case=False, na=False)]
    
    # riceCake = data[data["Item Name"].str.contains(r"Brown Sugar Rice Cake", case=False, na=False)].sum()
    # bingsu = data[data["Item Name"].str.contains(r"Bingsu", case=False, na=False)].sum()
    # ramen = data[data["Item Name"].str.contains(r"(?<!tossed )ramen", case=False, na=False)].sum()
    
    # data = pd.DataFrame({"Item Name":["Brown Sugar Rice Cake","Bingsu","Ramen"],
    #                      "Amount":[riceCake[4],bingsu[4],ramen[4]],
    #                      "Count":[riceCake[3],bingsu[3],ramen[3]]})
elif option == "Appetizers":
    data = data[data["Item Name"].str.contains(r"(Wonton(?! soup))|(Bingsu)", case=False, na=False)]
    
control = st.segmented_control('Display',["By Revenue","By Quantity"])
if control == "By Revenue":
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
    st.write("### 🏆 Top Most Popular Items")
    st.dataframe(top5["Item Name"])

# # Define a rainbow color sequence
# rainbow_colors = [
#     '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#EE82EE'
# ]

# # Create Altair chart with custom color scale
# chart = alt.Chart(data).mark_bar().encode(
#     x='Item Name',
#     y=displayColumn,
#     color=alt.Color('Category:N', scale=alt.Scale(range=rainbow_colors), legend=None)
# )

# st.altair_chart(chart)

