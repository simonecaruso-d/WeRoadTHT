# Environment Setting
import streamlit as st

import modules.oneConfiguration as Config

# Top Bar
def TopBar(logoUrl):
    st.set_page_config(page_title='WeRoad THT', page_icon='🔬', layout='wide')
    
    st.markdown(f"""<style>
    [data-testid="stAppViewContainer"] {{ background-color: {Config.ColorBackground}; }}
    [data-testid="stMainBlockContainer"] {{ background-color: {Config.ColorBackground}; }}
    .stApp {{ background-color: {Config.ColorBackground}; }}
    .topbar {{position: sticky; top: 0; display: flex; align-items: center; justify-content: space-between; padding: 16px 32px; background-color: {Config.ColorTopBar}; border-bottom: 2px solid {Config.ColorPrimary}; z-index: 999; margin-bottom: 20px;}}
    .logo {{ height: 32px; border-radius: 4px; }}
    .title {{ font-size: 20px; font-weight: 600; color: {Config.ColorPrimary}; margin: 0; }}
    .title-accent {{ color: {Config.ColorPrimary}; }}
    .status-badge {{ font-size: 15px; color: {Config.ColorText}; }}
    </style>""", unsafe_allow_html=True)

    logoHtml = f'<img src="{logoUrl}" class="logo" alt="WeRoad">' if logoUrl else ''
    st.markdown(f"""<div class="topbar"><div style="display: flex; align-items: center; gap: 12px;">{logoHtml}<div class="title"><span class="title-accent">●</span> WeRoad Take Home Test</div></div><div class="status-badge">Author: Simone Caruso</div></div>""", unsafe_allow_html=True) 

    return

# Table
def RenderTable(df, title=None):
    if title: st.markdown(f'<h3 style="color: {Config.ColorCACSecondary}; margin-top: 20px;">{title}</h3>', unsafe_allow_html=True)
    
    st.markdown(f"""<style>
    .table-container {{max-height: 500px; overflow-y: auto; border: 1px solid {Config.ColorCACSecondary}; border-radius: 6px;}}
    .custom-table {{width: 100%; border-collapse: collapse; font-size: 13px; border: none;}}
    .custom-table thead {{position: sticky; top: 0; background-color: {Config.ColorCACSecondary}; z-index: 10;}}
    .custom-table thead tr {{background-color: {Config.ColorCACSecondary};}}
    .custom-table th {{color: {Config.ColorWhite}; padding: 12px; text-align: left; font-weight: 600; border: none;}}
    .custom-table td {{padding: 10px 12px; color: {Config.ColorText}; border-bottom: 1px solid rgba(243, 156, 18, 0.1);}}
    .custom-table tr:hover td {{background-color: rgba(243, 156, 18, 0.05);}}
    </style>""", unsafe_allow_html=True)
    
    htmlTable             = '<table class="custom-table"><thead><tr>'
    for col in df.columns : htmlTable += f'<th>{col}</th>'
    htmlTable             += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        htmlTable += '<tr>'
        for val in row: htmlTable += f'<td>{str(val)}</td>'
        htmlTable += '</tr>'
    
    htmlTable += '</tbody></table>'
    
    st.markdown(f'<div class="table-container">{htmlTable}</div>', unsafe_allow_html=True)

    return

# Filter
def RenderFilter(availableValues, label='Select'):
    st.markdown(f'<p style="font-size: 14px; font-weight: 600; color: {Config.ColorText}; margin-bottom: 8px;">{label}</p>', unsafe_allow_html=True)
        
    st.markdown(f"""<style>
    [data-testid="stSelectbox"] {{background-color: {Config.ColorBackground} !important;}}
    [data-testid="stSelectbox"] > div {{background-color: {Config.ColorBackground} !important; border: 1.5px solid {Config.ColorPrimary} !important; border-radius: 6px !important;}}
    [data-testid="stSelectbox"] input {{background-color: {Config.ColorBackground} !important; color: {Config.ColorText} !important;}}
    [data-testid="stSelectbox"] button {{background-color: {Config.ColorBackground} !important; color: {Config.ColorPrimary} !important;}}
    </style>""", unsafe_allow_html=True)
    
    selectedValue = st.selectbox(label, availableValues, label_visibility='collapsed')
    
    return selectedValue

# Channel Plot
def RenderChannelVsCostPlot(fig, channel, lag, performanceType):
    fig.update_layout(
        title         = dict(text=f'{channel} {performanceType} vs Costs with {lag} weeks of lag', font=dict(size=16, color=Config.ColorPrimary)),
        xaxis         = dict(tickfont=dict(color=Config.ColorText), gridcolor=Config.ColorGrayLight, showgrid=True),
        yaxis         = dict(title=dict(text='Cost (€)', font=dict(color=Config.ColorPrimary)), tickfont=dict(color=Config.ColorText), gridcolor=Config.ColorGrayLight, showgrid=True),
        yaxis2        = dict(title=dict(text=performanceType, font=dict(color=Config.ColorSecondary)), tickfont=dict(color=Config.ColorText), anchor='x', overlaying='y', side='right'),
        hovermode     = 'x unified',
        plot_bgcolor  = Config.ColorBackground,
        paper_bgcolor = Config.ColorBackground,
        legend        = dict(x=0.01, y=0.99, font=dict(color=Config.ColorText)), 
        margin        = dict(l=60, r=60, t=80, b=60), 
        height        = 500)
    
    fig.update_traces(line=dict(width=2), marker=dict(size=6), selector=dict(mode='lines+markers'))
    
    fig.data[0].line.color = Config.ColorPrimary
    fig.data[1].line.color = Config.ColorSecondary
    
    return fig

# CAC Plot
def RenderCACPlot(fig, channel):
    fig.update_layout(
        title         = dict(text=f'{channel} CAC Evolution', font=dict(size=16, color=Config.ColorCACPrimary)),
        xaxis         = dict(tickfont=dict(color=Config.ColorText), gridcolor=Config.ColorGrayLight, showgrid=True),
        yaxis         = dict(title=dict(text='CAC (€)', font=dict(color=Config.ColorCACPrimary)), tickfont=dict(color=Config.ColorText), gridcolor=Config.ColorGrayLight, showgrid=True),
        hovermode     = 'x unified',
        plot_bgcolor  = Config.ColorBackground,
        paper_bgcolor = Config.ColorBackground,
        legend        = dict(x=0.01, y=0.99, font=dict(color=Config.ColorText)), 
        margin        = dict(l=60, r=60, t=80, b=60), 
        height        = 500)
    
    fig.update_traces(marker=dict(color=Config.ColorCACPrimary))
    
    return fig