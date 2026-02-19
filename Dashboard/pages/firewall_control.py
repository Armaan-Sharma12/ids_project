import streamlit as st
from components import navbar, sidebar
from utils import require_auth

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("🔥 Firewall Control Panel")
    st.markdown("Monitor and manage firewall status")
    
    st.markdown("---")
    
    if 'firewall_status' not in st.session_state:
        st.session_state.firewall_status = 'active'
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.firewall_status == 'active':
            st.markdown("""
            <div style='background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; 
                        border-radius: 12px; padding: 24px; text-align: center;'>
                <div style='font-size: 48px; margin-bottom: 12px;'>🟢</div>
                <h3 style='color: #10b981; margin-bottom: 8px;'>ACTIVE</h3>
                <p style='color: #a0aec0; font-size: 14px;'>Firewall is running</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; 
                        border-radius: 12px; padding: 24px; text-align: center;'>
                <div style='font-size: 48px; margin-bottom: 12px;'>🔴</div>
                <h3 style='color: #ef4444; margin-bottom: 8px;'>INACTIVE</h3>
                <p style='color: #a0aec0; font-size: 14px;'>Firewall is stopped</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Events Processed", "24,583")
        st.metric("Threats Blocked", "1,247")
    
    with col3:
        st.metric("Uptime", "99.98%")
        st.metric("Response Time", "< 1ms")
    
    st.markdown("---")
    
    st.markdown("### Control Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start Firewall", key="start_firewall", use_container_width=True, 
                    disabled=(st.session_state.firewall_status == 'active')):
            st.session_state.firewall_status = 'active'
            st.success("✅ Firewall started successfully")
            st.rerun()
    
    with col2:
        if st.button("⏸️ Stop Firewall", key="stop_firewall", use_container_width=True,
                    disabled=(st.session_state.firewall_status == 'inactive')):
            st.session_state.firewall_status = 'inactive'
            st.warning("⚠️ Firewall stopped")
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Firewall Statistics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Performance", "🛡️ Protection", "⚙️ Configuration"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
                <h4 style='color: #3b82f6;'>Processing Speed</h4>
                <p style='color: #a0aec0; margin-top: 12px;'>
                    <strong style='font-size: 24px; color: white;'>10,000+</strong><br>
                    Packets per second
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
                <h4 style='color: #10b981;'>Efficiency</h4>
                <p style='color: #a0aec0; margin-top: 12px;'>
                    <strong style='font-size: 24px; color: white;'>99.9%</strong><br>
                    Threat detection rate
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        #### Active Protection Features
        
        - ✅ DDoS Protection
        - ✅ Port Scanning Detection
        - ✅ SQL Injection Prevention
        - ✅ XSS Attack Blocking
        - ✅ Brute Force Protection
        - ✅ Zero-Day Threat Detection
        """)
    
    with tab3:
        st.markdown("""
        #### Current Configuration
        
        **Mode:** Autonomous Detection & Response  
        **Threshold:** High Confidence (>85%)  
        **Action:** Auto-Block Threats  
        **Logging:** Enabled  
        **Alerts:** Real-time  
        **Integration:** MongoDB Atlas  
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; 
                border-radius: 8px; padding: 16px;'>
        <h4 style='color: #3b82f6; margin-bottom: 8px;'>ℹ️ Firewall Information</h4>
        <p style='color: #a0aec0; font-size: 14px;'>
            This interface displays the status of your detection engine. The actual packet
            monitoring and threat blocking is handled by your separate Python detection engine
            that logs events to MongoDB. This dashboard provides monitoring and visualization
            of those events.
        </p>
    </div>
    """, unsafe_allow_html=True)