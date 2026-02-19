import streamlit as st
from components import navbar
from auth import register_user
from utils import navigate_to

def render():
    navbar.render()
    
    st.markdown("<h1 style='text-align: center;'>📝 Create Account</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0aec0;'>Join CyberShield and start protecting your infrastructure</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("signup_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            license_key = st.text_input("License Key", placeholder="Enter your license key")
            
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if not username or not password or not confirm_password or not license_key:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = register_user(username, password, license_key)
                    if success:
                        st.success(message)
                        st.info("Redirecting to sign in...")
                        st.balloons()
                        navigate_to('signin')
                    else:
                        st.error(message)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Already have an account?</p>", unsafe_allow_html=True)
        
        if st.button("Sign In", key="signup_to_signin", use_container_width=True):
            navigate_to('signin')
        
        if st.button("Back to Home", key="signup_to_home", use_container_width=True):
            navigate_to('home')
        
        st.markdown("---")
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; 
                    border-radius: 8px; padding: 16px; margin-top: 24px;'>
            <h4 style='color: #3b82f6; margin-bottom: 8px;'>📌 License Key Required</h4>
            <p style='color: #a0aec0; font-size: 14px;'>
                You need a valid license key to create an account. Contact your administrator
                or purchase a license from our website.
            </p>
        </div>
        """, unsafe_allow_html=True)