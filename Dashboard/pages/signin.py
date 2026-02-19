import streamlit as st
from components import navbar
from auth import authenticate
from utils import navigate_to

def render():
    navbar.render()
    
    st.markdown("<h1 style='text-align: center;'>🔐 Sign In</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0aec0;'>Access your CyberShield dashboard</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("signin_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    success, role = authenticate(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = role
                        st.success("Login successful! Redirecting...")
                        navigate_to('dashboard_home')
                        
                    else:
                        st.error("Invalid username or password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Don't have an account?</p>", unsafe_allow_html=True)
        
        if st.button("Create Account", key="signin_to_signup", use_container_width=True):
            navigate_to('signup')
        
        if st.button("Back to Home", key="signin_to_home", use_container_width=True):
            navigate_to('home')