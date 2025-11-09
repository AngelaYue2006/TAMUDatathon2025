import streamlit as st

st.set_page_config(page_title="Mai Shan Yun Dashboard", layout="wide")


# -----------------------------
# HOME PAGE LAYOUT
# -----------------------------
    # Create two columns: image on left (1/3), text on right (2/3)
col1, col2 = st.columns([1.5, 2], gap="large")

with col1:
    # Smaller image on the left
    st.image("assets/logo1.png")

with col2:

    st.markdown(
        """
        <div style="margin-top: 150px;">
            <h1 style='font-size:60px; color:#E0E0E0;'>MAI SHAN YUN</h1>
            <h2 style='font-size:40px; color:#A6824C;'>DASHBOARD</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add some spacing
    st.write("\n" * 3)
    # Continue button under the text
    # if st.button("Overview ->"):
    #     page = "1_Overview"

    st.write("Use navigation bar on the left-hand side to see an overview!")