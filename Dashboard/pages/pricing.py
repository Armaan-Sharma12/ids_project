import streamlit as st

def show_pricing():

    st.title("Pricing")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Basic")
        st.write("$10/month")

    with col2:
        st.subheader("Pro")
        st.write("$25/month")

    with col3:
        st.subheader("Enterprise")
        st.write("$100/month")
