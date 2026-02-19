import streamlit as st
from components import navbar, sidebar, charts
from utils import require_auth
import db

def render():
    require_auth()
    navbar.render()
    sidebar.render()
    
    st.title("📈 Advanced Analytics")
    st.markdown("Deep dive into security trends and patterns")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📉 Trends"])
    
    with tab1:
        st.markdown("### Attack Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            attack_dist = db.get_attack_distribution()
            charts.render_pie_chart(attack_dist, "Attack Type Distribution")
        
        with col2:
            st.markdown("#### Key Insights")
            
            total = sum([item['count'] for item in attack_dist]) if attack_dist else 0
            
            if attack_dist and total > 0:
                for item in attack_dist:
                    percentage = (item['count'] / total) * 100
                    st.markdown(f"""
                    <div style='background: #141b2d; padding: 16px; border-radius: 8px; 
                                margin-bottom: 12px; border: 1px solid #2d3748;'>
                        <strong style='color: #3b82f6;'>{item['_id']}</strong>
                        <div style='color: #a0aec0; margin-top: 4px;'>
                            {item['count']} events ({percentage:.1f}%)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        st.markdown("### Timeline Analysis")
        attack_timeline = db.get_attack_timeline()
        charts.render_line_chart(attack_timeline, "Attack Frequency Over Time")
    
    with tab2:
        st.markdown("### Detailed Threat Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_events = db.get_logs_count()
            st.metric("Total Events", total_events)
        
        with col2:
            blocked = db.get_blocked_attacks_count()
            st.metric("Blocked", blocked)
        
        with col3:
            if total_events > 0:
                block_rate = (blocked / total_events) * 100
                st.metric("Block Rate", f"{block_rate:.1f}%")
            else:
                st.metric("Block Rate", "0%")
        
        st.markdown("---")
        
        st.markdown("### Top Threat Sources")
        
        logs = db.get_logs(limit=1000)
        
        if logs:
            from collections import Counter
            ip_counts = Counter([log.get('src_ip') for log in logs if log.get('src_ip')])
            top_ips = ip_counts.most_common(10)
            
            if top_ips:
                ip_data = [{'_id': ip, 'count': count} for ip, count in top_ips]
                charts.render_bar_chart(ip_data, "Top 10 Source IPs by Event Count")
            else:
                st.info("No IP data available")
        else:
            st.info("No log data available")
    
    with tab3:
        st.markdown("### Security Trends")
        
        st.markdown("#### 24-Hour Activity")
        attack_timeline = db.get_attack_timeline()
        charts.render_line_chart(attack_timeline, "Event Timeline")
        
        st.markdown("---")
        
        st.markdown("#### Summary Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: #141b2d; padding: 24px; border-radius: 12px; 
                        border: 1px solid #2d3748;'>
                <h4 style='color: #3b82f6; margin-bottom: 16px;'>🎯 Detection Accuracy</h4>
                <p style='color: #a0aec0;'>
                    AI models achieving high confidence scores with minimal false positives.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #141b2d; padding: 24px; border-radius: 12px; 
                        border: 1px solid #2d3748;'>
                <h4 style='color: #10b981; margin-bottom: 16px;'>⚡ Response Time</h4>
                <p style='color: #a0aec0;'>
                    Automated response system blocking threats in real-time.
                </p>
            </div>
            """, unsafe_allow_html=True)