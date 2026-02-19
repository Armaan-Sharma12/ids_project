import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_pie_chart(data, title):
    if not data:
        st.info("No data available")
        return
    
    labels = [item['_id'] for item in data]
    values = [item['count'] for item in data]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=['#3b82f6', '#10b981', '#ef4444', '#f59e0b'])
    )])
    
    fig.update_layout(
        title=title,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_line_chart(data, title):
    if not data:
        st.info("No data available")
        return
    
    df = pd.DataFrame(data)
    df.columns = ['timestamp', 'count']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['count'],
        mode='lines+markers',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Count",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        xaxis=dict(showgrid=True, gridcolor='#2d3748'),
        yaxis=dict(showgrid=True, gridcolor='#2d3748')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(data, title):
    if not data:
        st.info("No data available")
        return
    
    df = pd.DataFrame(data)
    df.columns = ['category', 'count']
    
    fig = go.Figure(data=[go.Bar(
        x=df['category'],
        y=df['count'],
        marker=dict(color='#10b981')
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Category",
        yaxis_title="Count",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        xaxis=dict(showgrid=True, gridcolor='#2d3748'),
        yaxis=dict(showgrid=True, gridcolor='#2d3748')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_metric_cards(metrics):
    cols = st.columns(len(metrics))
    
    for idx, (label, value, delta, icon) in enumerate(metrics):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #141b2d, #1f2937); 
                        border-radius: 12px; padding: 24px; border: 1px solid #2d3748;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
                <div style="font-size: 36px; margin-bottom: 8px;">{icon}</div>
                <div style="color: #a0aec0; font-size: 14px; margin-bottom: 4px;">{label}</div>
                <div style="font-size: 32px; font-weight: 700; color: white;">{value}</div>
                {f'<div style="color: #10b981; font-size: 14px; margin-top: 4px;">↑ {delta}</div>' if delta else ''}
            </div>
            """, unsafe_allow_html=True)