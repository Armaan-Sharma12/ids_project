from datetime import datetime
import streamlit as st

def format_timestamp(timestamp):
    if isinstance(timestamp, str):
        return timestamp
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = 'home'
    st.rerun()

def require_auth():
    if not st.session_state.logged_in:
        navigate_to('signin')
        st.stop()

def require_admin():
    require_auth()
    if st.session_state.role != 'admin':
        st.error("Access denied. Admin privileges required.")
        st.stop()