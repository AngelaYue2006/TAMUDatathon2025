import streamlit as st 
import chat

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
        
st.header("Trend")
# TODO fill out this line chart with data across months!
st.line_chart()
