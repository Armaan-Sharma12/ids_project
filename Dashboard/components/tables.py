import streamlit as st
import pandas as pd
from utils import format_timestamp

def render_logs_table(logs, limit=50):
    if not logs:
        st.info("No logs available")
        return
    
    data = []
    for log in logs[:limit]:
        data.append({
            'Timestamp': format_timestamp(log.get('timestamp', 'N/A')),
            'Source IP': log.get('src_ip', 'N/A'),
            'Label': log.get('label', 'N/A'),
            'Confidence': f"{log.get('confidence', 0):.2f}",
            'Action': log.get('action', 'N/A'),
            'Reason': log.get('reason', 'N/A')
        })
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

def render_blocked_ips_table(blocked_ips):
    if not blocked_ips:
        st.info("No blocked IPs")
        return
    
    data = []
    for item in blocked_ips:
        data.append({
            'IP Address': item.get('ip', 'N/A'),
            'Reason': item.get('reason', 'N/A'),
            'Blocked At': format_timestamp(item.get('blocked_at', 'N/A'))
        })
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

def render_users_table(users):
    if not users:
        st.info("No users found")
        return
    
    data = []
    for user in users:
        data.append({
            'Username': user.get('username', 'N/A'),
            'Role': user.get('role', 'N/A'),
            'License Active': '✅' if user.get('license_active') else '❌',
            'Created At': format_timestamp(user.get('created_at', 'N/A'))
        })
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )