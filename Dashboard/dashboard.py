import streamlit as st
from pages import home, signin, signup, dashboard_home, analytics, logs, alerts, blocked_ips, firewall_control, license, profile, admin

st.set_page_config(
    page_title="CyberShield AI Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open('Dashboard/assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'role' not in st.session_state:
    st.session_state.role = None

page_map = {
    'home': home,
    'signin': signin,
    'signup': signup,
    'dashboard_home': dashboard_home,
    'analytics': analytics,
    'logs': logs,
    'alerts': alerts,
    'blocked_ips': blocked_ips,
    'firewall_control': firewall_control,
    'license': license,
    'profile': profile,
    'admin': admin
}

if st.session_state.page in page_map:
    page_map[st.session_state.page].render()
else:
    home.render()