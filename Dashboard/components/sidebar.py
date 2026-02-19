import streamlit as st
from utils import navigate_to

def render():
    st.sidebar.markdown("### 🛡️ Navigation")
    st.sidebar.markdown("---")
    
    menu_items = [
        ("📊 Dashboard", "dashboard_home"),
        ("📈 Analytics", "analytics"),
        ("📋 Logs", "logs"),
        ("🚨 Alerts", "alerts"),
        ("🚫 Blocked IPs", "blocked_ips"),
        ("🔥 Firewall Control", "firewall_control"),
        ("🎫 License", "license"),
        ("👤 Profile", "profile")
    ]
    
    if st.session_state.role == 'admin':
        menu_items.append(("⚙️ Admin Panel", "admin"))
    
    for label, page_key in menu_items:
        if st.sidebar.button(label, key=f"sidebar_{page_key}", use_container_width=True):
            navigate_to(page_key)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**User:** {st.session_state.username}")
    st.sidebar.markdown(f"**Role:** {st.session_state.role}")