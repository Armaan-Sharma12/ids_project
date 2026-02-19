import streamlit as st
from components import navbar, sidebar, tables
from utils import require_auth
import db

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("🚫 Blocked IP Addresses")
    st.markdown("Manage and monitor blocked threat sources")
    
    st.markdown("---")
    
    blocked_ips = db.get_blocked_ips()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Blocked", len(blocked_ips))
    
    with col2:
        recent_blocks = len([ip for ip in blocked_ips[:10]])
        st.metric("Recent (Last 10)", recent_blocks)
    
    with col3:
        st.metric("Status", "🛡️ Protected")
    
    st.markdown("---")
    
    if blocked_ips:
        st.markdown("### Blocked IP List")
        
        tables.render_blocked_ips_table(blocked_ips)
        
        st.markdown("---")
        
        st.markdown("### 🔧 Management Actions")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            ip_to_unblock = st.text_input("Enter IP address to unblock:", placeholder="e.g., 192.168.1.100", key="ip_unblock_input")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Unblock IP", key="unblock_ip_btn", use_container_width=True):
                if ip_to_unblock:
                    if any(item.get('ip') == ip_to_unblock for item in blocked_ips):
                        db.unblock_ip(ip_to_unblock)
                        st.success(f"✅ IP {ip_to_unblock} has been unblocked")
                        st.rerun()
                    else:
                        st.error(f"IP {ip_to_unblock} is not in the blocked list")
                else:
                    st.warning("Please enter an IP address")
    else:
        st.info("✅ No blocked IP addresses at this time")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh List", key="refresh_blocked_ips", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; 
                border-radius: 8px; padding: 16px;'>
        <h4 style='color: #ef4444; margin-bottom: 8px;'>⚠️ Important Notice</h4>
        <p style='color: #a0aec0; font-size: 14px;'>
            Blocked IPs are automatically added when the AI detection system identifies
            high-confidence threats. Unblocking an IP address should only be done if you're
            certain it's a false positive or the threat has been resolved.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("ℹ️ About IP Blocking"):
        st.markdown("""
        **How IP Blocking Works:**
        
        1. **Detection**: AI models analyze network traffic in real-time
        2. **Classification**: Threats are identified with confidence scores
        3. **Action**: High-confidence threats (>85%) trigger automatic blocking
        4. **Logging**: All blocks are recorded with timestamps and reasons
        
        **Best Practices:**
        - Review blocked IPs regularly
        - Investigate patterns in blocked sources
        - Unblock IPs only when necessary
        - Monitor for repeated blocking attempts
        """)