import streamlit as st
from utils import navigate_to, logout

def render():
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        st.markdown("### 🛡️ CyberShield")
    
    with col3:
        if st.session_state.logged_in:
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**{st.session_state.username}**")
            with col_b:
                if st.button("Logout", key="nav_logout"):
                    logout()
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign In", key="nav_signin"):
                    navigate_to('signin')
            with col_b:
                if st.button("Sign Up", key="nav_signup"):
                    navigate_to('signup')
    
    st.markdown("---")