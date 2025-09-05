import streamlit as st

@st.cache_resource
def get_db_connection():
    return st.connection("mysql", type="sql")