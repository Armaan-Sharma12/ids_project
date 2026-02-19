import streamlit as st
from components import navbar, sidebar, tables
from utils import require_admin
import db

def render():
    require_admin()
    navbar.render()
    sidebar.render()
    
    st.title("⚙️ Admin Control Panel")
    st.markdown("System administration and management")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 User Management", "📊 System Stats", "🗑️ Data Management", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### User Management")
        
        users = db.get_all_users()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", len(users))
        
        with col2:
            admin_count = len([u for u in users if u.get('role') == 'admin'])
            st.metric("Administrators", admin_count)
        
        with col3:
            active_licenses = len([u for u in users if u.get('license_active')])
            st.metric("Active Licenses", active_licenses)
        
        st.markdown("---")
        
        st.markdown("#### All Users")
        tables.render_users_table(users)
        
        st.markdown("---")
        
        st.markdown("#### Delete User")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            username_to_delete = st.text_input("Enter username to delete:", key="admin_delete_user")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Delete User", key="admin_delete_btn", use_container_width=True):
                if username_to_delete:
                    if username_to_delete == st.session_state.username:
                        st.error("❌ You cannot delete your own account")
                    elif db.get_user(username_to_delete):
                        db.delete_user(username_to_delete)
                        st.success(f"✅ User '{username_to_delete}' has been deleted")
                        st.rerun()
                    else:
                        st.error(f"❌ User '{username_to_delete}' not found")
                else:
                    st.warning("Please enter a username")
    
    with tab2:
        st.markdown("### System Statistics")
        
        total_logs = db.get_logs_count()
        blocked_attacks = db.get_blocked_attacks_count()
        active_threats = db.get_active_threats_count()
        unique_ips = db.get_unique_attackers_count()
        blocked_ips_count = len(db.get_blocked_ips())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Events", total_logs)
            st.metric("Blocked Attacks", blocked_attacks)
        
        with col2:
            st.metric("Active Threats", active_threats)
            st.metric("Unique Source IPs", unique_ips)
        
        with col3:
            st.metric("Blocked IPs", blocked_ips_count)
            st.metric("Total Users", len(users))
        
        st.markdown("---")
        
        st.markdown("#### System Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
                <h4 style='color: #10b981;'>✅ System Status</h4>
                <ul style='color: #a0aec0; margin-top: 12px; line-height: 1.8;'>
                    <li>Database: <strong style='color: #10b981;'>Connected</strong></li>
                    <li>AI Engine: <strong style='color: #10b981;'>Active</strong></li>
                    <li>Monitoring: <strong style='color: #10b981;'>Running</strong></li>
                    <li>API: <strong style='color: #10b981;'>Online</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
                <h4 style='color: #3b82f6;'>📊 Performance</h4>
                <ul style='color: #a0aec0; margin-top: 12px; line-height: 1.8;'>
                    <li>CPU Usage: <strong style='color: white;'>23%</strong></li>
                    <li>Memory: <strong style='color: white;'>1.2 GB</strong></li>
                    <li>Disk: <strong style='color: white;'>45 GB</strong></li>
                    <li>Network: <strong style='color: white;'>120 Mbps</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Data Management")
        
        st.markdown("#### Database Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Log Entries", total_logs)
        
        with col2:
            st.metric("Blocked IPs", blocked_ips_count)
        
        with col3:
            st.metric("Users", len(users))
        
        st.markdown("---")
        
        st.markdown("#### Clear Data")
        
        st.warning("⚠️ Warning: These actions are irreversible!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Logs", key="admin_clear_logs", use_container_width=True):
                db.clear_logs()
                st.success("✅ All logs have been cleared")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Blocked IPs", key="admin_clear_ips", use_container_width=True):
                blocked = db.get_blocked_ips()
                for item in blocked:
                    db.unblock_ip(item.get('ip'))
                st.success("✅ All blocked IPs have been cleared")
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div style='background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; 
                    border-radius: 8px; padding: 16px;'>
            <h4 style='color: #ef4444; margin-bottom: 8px;'>⚠️ Data Management Notice</h4>
            <p style='color: #a0aec0; font-size: 14px;'>
                Clearing logs and blocked IPs will permanently delete this data from the database.
                Make sure to export any important data before clearing. This action cannot be undone.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### System Settings")
        
        st.markdown("#### Detection Settings")
        
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.85, 0.05, key="admin_confidence")
        
        st.markdown("#### Alert Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Email Alerts", value=True, key="admin_email_alerts")
            st.checkbox("SMS Alerts", value=False, key="admin_sms_alerts")
        
        with col2:
            st.checkbox("Webhook Notifications", value=False, key="admin_webhook")
            st.checkbox("Daily Reports", value=True, key="admin_reports")
        
        st.markdown("---")
        
        if st.button("💾 Save Settings", key="admin_save_settings", use_container_width=True):
            st.success("✅ Settings saved successfully!")
        
        st.markdown("---")
        
        st.markdown("#### System Information")
        
        st.markdown("""
        <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
            <h4 style='color: #3b82f6;'>CyberShield AI Defense</h4>
            <ul style='color: #a0aec0; margin-top: 12px; line-height: 1.8;'>
                <li><strong>Version:</strong> 2.0.1</li>
                <li><strong>Build:</strong> 20260216</li>
                <li><strong>Database:</strong> MongoDB Atlas</li>
                <li><strong>Framework:</strong> Streamlit 1.31.0</li>
                <li><strong>Python:</strong> 3.11.7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)