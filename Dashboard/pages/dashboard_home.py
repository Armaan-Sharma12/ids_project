import streamlit as st
from components import navbar, sidebar, charts, tables
from utils import require_auth
import db

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("🛡️ Dashboard Overview")
    st.markdown("Real-time security monitoring and threat intelligence")
    
    st.markdown("---")
    
    total_attacks = db.get_logs_count()
    blocked_attacks = db.get_blocked_attacks_count()
    active_threats = db.get_active_threats_count()
    unique_attackers = db.get_unique_attackers_count()
    
    metrics = [
        ("Total Events", total_attacks, None, "📊"),
        ("Blocked Attacks", blocked_attacks, None, "🛡️"),
        ("Active Threats", active_threats, None, "🚨"),
        ("Unique IPs", unique_attackers, None, "🌐")
    ]
    
    charts.render_metric_cards(metrics)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Attack Distribution")
        attack_dist = db.get_attack_distribution()
        charts.render_pie_chart(attack_dist, "Attack Types")
    
    with col2:
        st.markdown("### 📈 Attack Timeline (Last 24h)")
        attack_timeline = db.get_attack_timeline()
        charts.render_line_chart(attack_timeline, "Attacks Over Time")
    
    st.markdown("---")
    
    st.markdown("### 📋 Recent Security Events")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        log_limit = st.selectbox("Show entries:", [10, 25, 50, 100], index=1, key="dashboard_log_limit")
    
    logs = db.get_logs(limit=log_limit)
    tables.render_logs_table(logs, limit=log_limit)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 View Analytics", use_container_width=True, key="dash_to_analytics"):
            st.session_state.page = 'analytics'
            st.rerun()
    
    with col2:
        if st.button("📋 View All Logs", use_container_width=True, key="dash_to_logs"):
            st.session_state.page = 'logs'
            st.rerun()
    
    with col3:
        if st.button("🚫 Blocked IPs", use_container_width=True, key="dash_to_blocked"):
            st.session_state.page = 'blocked_ips'
            st.rerun()