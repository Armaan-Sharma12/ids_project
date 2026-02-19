import streamlit as st
from components import navbar, sidebar
from utils import require_auth
import db

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("🚨 Active Alerts")
    st.markdown("Real-time critical security alerts and notifications")
    
    st.markdown("---")
    
    logs = db.get_logs(limit=100)
    
    high_confidence_threats = [
        log for log in logs 
        if log.get('label') == 'attack' and log.get('confidence', 0) > 0.8
    ]
    
    critical_alerts = high_confidence_threats[:20]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Alerts", len(critical_alerts))
    
    with col2:
        critical_count = len([a for a in critical_alerts if a.get('confidence', 0) > 0.95])
        st.metric("Critical", critical_count)
    
    with col3:
        blocked_count = len([a for a in critical_alerts if a.get('action') == 'blocked'])
        st.metric("Mitigated", blocked_count)
    
    st.markdown("---")
    
    if critical_alerts:
        st.markdown("### 🔴 Critical Alerts (Confidence > 80%)")
        
        for idx, alert in enumerate(critical_alerts):
            confidence = alert.get('confidence', 0)
            
            if confidence > 0.95:
                color = "#ef4444"
                severity = "CRITICAL"
            elif confidence > 0.85:
                color = "#f59e0b"
                severity = "HIGH"
            else:
                color = "#3b82f6"
                severity = "MEDIUM"
            
            st.markdown(f"""
            <div style='background: #141b2d; border-left: 4px solid {color}; 
                        padding: 16px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='color: {color}; font-size: 16px;'>{severity}</strong>
                        <span style='color: #a0aec0; margin-left: 12px;'>
                            {alert.get('timestamp', 'N/A')}
                        </span>
                    </div>
                    <div>
                        <span style='background: {color}; color: white; padding: 4px 12px; 
                                    border-radius: 12px; font-size: 12px; font-weight: 600;'>
                            {confidence:.1%}
                        </span>
                    </div>
                </div>
                <div style='margin-top: 12px; color: #a0aec0;'>
                    <strong>Source IP:</strong> {alert.get('src_ip', 'N/A')}<br>
                    <strong>Type:</strong> {alert.get('label', 'N/A')}<br>
                    <strong>Action:</strong> {alert.get('action', 'N/A')}<br>
                    <strong>Reason:</strong> {alert.get('reason', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical alerts at this time. System is secure.")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Alerts", key="refresh_alerts", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Alert Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
            <h4 style='color: #3b82f6;'>Alert Levels</h4>
            <ul style='color: #a0aec0; margin-top: 12px;'>
                <li><strong style='color: #ef4444;'>CRITICAL:</strong> Confidence > 95%</li>
                <li><strong style='color: #f59e0b;'>HIGH:</strong> Confidence 85-95%</li>
                <li><strong style='color: #3b82f6;'>MEDIUM:</strong> Confidence 80-85%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
            <h4 style='color: #10b981;'>Response Actions</h4>
            <ul style='color: #a0aec0; margin-top: 12px;'>
                <li><strong>Blocked:</strong> Traffic denied</li>
                <li><strong>Monitored:</strong> Under observation</li>
                <li><strong>Logged:</strong> Recorded for analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)