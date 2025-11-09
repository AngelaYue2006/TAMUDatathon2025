import streamlit as st 
import chat
import os
import pandas as pd
import altair as alt

# Add chatbot to this page's sidear
suggested_questions = [
    "What kind of sales should I expect for next month?"
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
        
st.header("Sales Over Time")
st.write("2025")
# TODO fill out this line chart with data across months!
folder = "data"
months = ["May","June","July","August","September","October"]

all_data = []
for month in months:
    month_file = f"{folder}/{month}/{month}_Data_Items.csv"
    if os.path.exists(month_file):
        df = pd.read_csv(month_file)
        # Convert dollar amounts to float
        df["Amount"] = (
            df["Amount"]
            .replace('[\$,]', '', regex=True)   # remove $ and ,
            .astype(float)                       # convert to float
            )
        df['Month'] = month
        all_data.append(df)
historical_data = pd.concat(all_data, ignore_index=True)





# display options
control = st.segmented_control('Display',["By Revenue","By Quantity"])
if control == "By Revenue":
    # Display by dollar value
    displayColumn = "Amount ($)"
else:
    # Display by quantity
    displayColumn = "Sales"
    
# Calculate data summary per month
summary = historical_data.groupby(['Month'],sort=False).agg(
    total_count=('Count','sum'),
    total_revenue=('Amount','sum')
).reset_index()
summary.rename(columns={'total_count':'Sales','total_revenue':"Amount ($)"},inplace=True)
chart = alt.Chart(summary).mark_line().encode(
    x=alt.X('Month:N',sort=summary["Month"].tolist()),
    y=f'{displayColumn}:Q',
)

st.altair_chart(chart)
#st.line_chart(summary,y="Sales",x="Month")


