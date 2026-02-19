import streamlit as st
from components import navbar, sidebar
from utils import require_auth
import db
from datetime import datetime

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("🎫 License Management")
    st.markdown("View and manage your CyberShield license")
    
    st.markdown("---")
    
    license_info = db.get_license_info(st.session_state.username)
    
    if license_info:
        is_active = license_info.get('active', False)
        expiry = license_info.get('expiry')
        license_key = license_info.get('license_key', 'N/A')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### License Details")
            
            st.markdown(f"""
            <div style='background: #141b2d; padding: 24px; border-radius: 12px; border: 1px solid #2d3748;'>
                <div style='margin-bottom: 16px;'>
                    <span style='color: #a0aec0;'>License Key:</span><br>
                    <strong style='color: white; font-size: 18px; font-family: monospace;'>{license_key}</strong>
                </div>
                <div style='margin-bottom: 16px;'>
                    <span style='color: #a0aec0;'>Status:</span><br>
                    <strong style='color: {"#10b981" if is_active else "#ef4444"}; font-size: 18px;'>
                        {"✅ ACTIVE" if is_active else "❌ INACTIVE"}
                    </strong>
                </div>
                <div style='margin-bottom: 16px;'>
                    <span style='color: #a0aec0;'>Assigned To:</span><br>
                    <strong style='color: white; font-size: 18px;'>{st.session_state.username}</strong>
                </div>
                <div>
                    <span style='color: #a0aec0;'>Expiry Date:</span><br>
                    <strong style='color: white; font-size: 18px;'>{expiry if expiry else "No expiry"}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if is_active:
                st.markdown("""
                <div style='background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; 
                            border-radius: 12px; padding: 24px; text-align: center;'>
                    <div style='font-size: 64px; margin-bottom: 16px;'>✅</div>
                    <h3 style='color: #10b981;'>VALID</h3>
                    <p style='color: #a0aec0; font-size: 14px; margin-top: 8px;'>
                        Your license is active and valid
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; 
                            border-radius: 12px; padding: 24px; text-align: center;'>
                    <div style='font-size: 64px; margin-bottom: 16px;'>❌</div>
                    <h3 style='color: #ef4444;'>EXPIRED</h3>
                    <p style='color: #a0aec0; font-size: 14px; margin-top: 8px;'>
                        Please renew your license
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### License Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
                <h4 style='color: #3b82f6; margin-bottom: 16px;'>✨ Included Features</h4>
                <ul style='color: #a0aec0; line-height: 1.8;'>
                    <li>Real-time threat detection</li>
                    <li>AI-powered analysis</li>
                    <li>Automated response system</li>
                    <li>Advanced analytics dashboard</li>
                    <li>Unlimited event logging</li>
                    <li>IP blocking & management</li>
                    <li>24/7 monitoring</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #141b2d; padding: 20px; border-radius: 8px; border: 1px solid #2d3748;'>
                <h4 style='color: #10b981; margin-bottom: 16px;'>📊 Usage Limits</h4>
                <div style='color: #a0aec0; line-height: 1.8;'>
                    <div style='margin-bottom: 12px;'>
                        <strong style='color: white;'>Events per day:</strong> Unlimited
                    </div>
                    <div style='margin-bottom: 12px;'>
                        <strong style='color: white;'>Data retention:</strong> 90 days
                    </div>
                    <div style='margin-bottom: 12px;'>
                        <strong style='color: white;'>Users:</strong> Single user
                    </div>
                    <div style='margin-bottom: 12px;'>
                        <strong style='color: white;'>Support:</strong> Email & Chat
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No license information found for your account")
    
    st.markdown("---")
    
    st.markdown("### 📞 Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Need help with your license?**
        
        - Email: support@cybershield.ai
        - Phone: 1-800-CYBER-AI
        - Chat: Available 24/7
        """)
    
    with col2:
        st.markdown("""
        **Renewal & Upgrades**
        
        - Visit our website to renew
        - Enterprise plans available
        - Volume discounts offered
        """)
    
    st.markdown("---")
    
    if st.button("🔄 Refresh License Info", key="refresh_license", use_container_width=True):
        st.rerun()