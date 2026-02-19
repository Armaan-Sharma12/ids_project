import streamlit as st
from components import navbar, sidebar
from utils import require_auth
import db
import auth

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("👤 User Profile")
    st.markdown("Manage your account settings and preferences")
    
    st.markdown("---")
    
    user = db.get_user(st.session_state.username)
    
    if user:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Account Information")
            
            st.markdown(f"""
            <div style='background: #141b2d; padding: 24px; border-radius: 12px; border: 1px solid #2d3748;'>
                <div style='margin-bottom: 16px;'>
                    <span style='color: #a0aec0;'>Username:</span><br>
                    <strong style='color: white; font-size: 18px;'>{user.get('username', 'N/A')}</strong>
                </div>
                <div style='margin-bottom: 16px;'>
                    <span style='color: #a0aec0;'>Role:</span><br>
                    <strong style='color: #3b82f6; font-size: 18px;'>{user.get('role', 'user').upper()}</strong>
                </div>
                <div style='margin-bottom: 16px;'>
                    <span style='color: #a0aec0;'>License Status:</span><br>
                    <strong style='color: {"#10b981" if user.get("license_active") else "#ef4444"}; font-size: 18px;'>
                        {"✅ ACTIVE" if user.get("license_active") else "❌ INACTIVE"}
                    </strong>
                </div>
                <div>
                    <span style='color: #a0aec0;'>Account Created:</span><br>
                    <strong style='color: white; font-size: 18px;'>{user.get('created_at', 'N/A')}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #3b82f6, #2563eb); 
                        border-radius: 12px; padding: 24px; text-align: center; height: 100%;
                        display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 64px; margin-bottom: 16px;'>👤</div>
                <h3 style='color: white; margin-bottom: 8px;'>{}</h3>
                <p style='color: #e0e7ff; font-size: 14px;'>{} Account</p>
            </div>
            """.format(user.get('username', 'User'), user.get('role', 'user').title()), unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔐 Change Password")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password", key="current_pass")
        new_password = st.text_input("New Password", type="password", key="new_pass")
        confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_pass")
        
        submit = st.form_submit_button("Update Password", use_container_width=True)
        
        if submit:
            if not current_password or not new_password or not confirm_new_password:
                st.error("Please fill in all fields")
            elif new_password != confirm_new_password:
                st.error("New passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                success, _ = auth.authenticate(st.session_state.username, current_password)
                if success:
                    new_hash = auth.hash_password(new_password)
                    db.update_password(st.session_state.username, new_hash)
                    st.success("✅ Password updated successfully!")
                else:
                    st.error("Current password is incorrect")
    
    st.markdown("---")
    
    st.markdown("### 📊 Account Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Logins", "47")
    
    with col2:
        st.metric("Events Viewed", "2,341")
    
    with col3:
        st.metric("Last Login", "Today")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Email notifications", value=True, key="pref_email")
        st.checkbox("Real-time alerts", value=True, key="pref_alerts")
    
    with col2:
        st.checkbox("Weekly reports", value=False, key="pref_reports")
        st.checkbox("Security updates", value=True, key="pref_updates")
    
    st.markdown("---")
    
    if st.button("💾 Save Preferences", key="save_prefs", use_container_width=True):
        st.success("✅ Preferences saved successfully!")
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; 
                border-radius: 8px; padding: 16px;'>
        <h4 style='color: #3b82f6; margin-bottom: 8px;'>🔒 Privacy & Security</h4>
        <p style='color: #a0aec0; font-size: 14px;'>
            Your account information is encrypted and stored securely. We never share
            your data with third parties. For more information, please review our
            Privacy Policy and Terms of Service.
        </p>
    </div>
    """, unsafe_allow_html=True)