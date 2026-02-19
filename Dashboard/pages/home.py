import streamlit as st
from components import navbar
from utils import navigate_to

def render():
    navbar.render()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); 
                padding: 80px 40px; border-radius: 16px; text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 56px; margin-bottom: 16px; color: white;">🛡️ CyberShield AI Defense</h1>
        <p style="font-size: 24px; color: #e0e7ff; margin-bottom: 32px;">
            Next-Generation Autonomous Cyber Defense Platform
        </p>
        <p style="font-size: 18px; color: #c7d2fe; max-width: 800px; margin: 0 auto;">
            Powered by advanced AI and machine learning, CyberShield provides real-time threat detection,
            automated response, and comprehensive security analytics for enterprise environments.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Started", key="home_get_started", use_container_width=True):
            navigate_to('signup')
    
    with col2:
        if st.button("Sign In", key="home_signin", use_container_width=True):
            navigate_to('signin')
    
    st.markdown("## Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #141b2d; border-radius: 12px; padding: 32px; 
                    border: 1px solid #2d3748; height: 100%;">
            <div style="font-size: 48px; margin-bottom: 16px;">🤖</div>
            <h3 style="color: white; margin-bottom: 16px;">AI-Powered Detection</h3>
            <p style="color: #a0aec0;">
                Advanced machine learning models identify threats with 99.8% accuracy
                and minimal false positives.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #141b2d; border-radius: 12px; padding: 32px; 
                    border: 1px solid #2d3748; height: 100%;">
            <div style="font-size: 48px; margin-bottom: 16px;">⚡</div>
            <h3 style="color: white; margin-bottom: 16px;">Real-Time Response</h3>
            <p style="color: #a0aec0;">
                Automated threat mitigation responds to attacks in milliseconds,
                blocking malicious actors before damage occurs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #141b2d; border-radius: 12px; padding: 32px; 
                    border: 1px solid #2d3748; height: 100%;">
            <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
            <h3 style="color: white; margin-bottom: 16px;">Advanced Analytics</h3>
            <p style="color: #a0aec0;">
                Comprehensive dashboards and reports provide deep insights into
                your security posture and threat landscape.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## Why Choose CyberShield?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Precision & Accuracy
        Our AI models are trained on millions of threat patterns, ensuring
        industry-leading detection rates with minimal false positives.
        
        ### 🚀 Scalable Architecture
        Built to protect everything from small businesses to Fortune 500
        enterprises with seamless scalability.
        """)
    
    with col2:
        st.markdown("""
        ### 🔒 Zero-Trust Security
        Implements comprehensive zero-trust principles with continuous
        verification and least-privilege access controls.
        
        ### 🌐 Cloud-Native Design
        Fully cloud-native architecture with multi-region deployment
        and 99.99% uptime SLA.
        """)
    
    st.markdown("---")
    
    st.markdown("## Trusted by Leading Organizations")
    
    st.markdown("""
    <div style="text-align: center; padding: 40px;">
        <p style="font-size: 18px; color: #a0aec0;">
            Join thousands of organizations worldwide that trust CyberShield
            to protect their critical infrastructure and data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Organizations Protected", "5,000+")
    
    with col2:
        st.metric("Threats Blocked Daily", "10M+")
    
    with col3:
        st.metric("Uptime SLA", "99.99%")