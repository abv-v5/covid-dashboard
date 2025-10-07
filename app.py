import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="COVID-19 Data Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotly {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Description
st.title("🦠 COVID-19 Global Data Analysis Dashboard")
st.markdown("Interactive visualization of country-wise COVID-19 statistics including confirmed cases, deaths, recoveries, and active cases.")

# Sidebar for User Controls
with st.sidebar:
    st.header("📊 Dashboard Controls")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload COVID-19 Dataset (CSV)", type=['csv'])
    
    # Number of countries to display
    top_n = st.slider("Select Top N Countries", 5, 30, 10)
    
    # Visualization type selector
    viz_type = st.multiselect(
        "Select Visualizations",
        ["Line Plot", "Bar Chart", "Pairplot", "Correlation Heatmap", "Regional Analysis"],
        default=["Line Plot", "Bar Chart"]
    )
    
    # Color palette selector
    color_palette = st.selectbox(
        "Choose Color Palette",
        ["bright", "deep", "muted", "pastel", "dark", "colorblind"]
    )

# Load Data Function
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # Load default dataset (add your CSV path)
        df = pd.read_csv('covid_19.csv')
    return df

# Main Dashboard Content
if uploaded_file is not None or True:  # Replace with your data loading logic
    df = load_data(uploaded_file)
    
    # Display basic statistics in columns
    st.header("📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Countries", len(df))
    with col2:
        st.metric("Total Confirmed", f"{df['Confirmed'].sum():,.0f}")
    with col3:
        st.metric("Total Deaths", f"{df['Deaths'].sum():,.0f}")
    with col4:
        st.metric("Total Recovered", f"{df['Recovered'].sum():,.0f}")
    
    st.write("---")
    
    # Top Countries Section
    st.header(f"🌍 Top {top_n} Most Affected Countries")
    top_countries = df.nlargest(top_n, 'Confirmed')
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts", "🔥 Heatmap", "🌐 Regional", "📋 Data Table"])
    
    with tab1:
        if "Line Plot" in viz_type:
            st.subheader("Confirmed Cases - Line Chart")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(top_countries['Country/Region'], top_countries['Confirmed'], 
                   marker='o', linewidth=2, markersize=8)
            ax.set_xlabel('Country', fontsize=12)
            ax.set_ylabel('Confirmed Cases', fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        
        if "Bar Chart" in viz_type:
            st.subheader("Active Cases - Bar Chart")
            fig = px.bar(top_countries, x='Country/Region', y='Active',
                        color='WHO Region',
                        title=f'Top {top_n} Countries by Active Cases',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if "Correlation Heatmap" in viz_type:
            st.subheader("🔥 Correlation Heatmap")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            corr = df[numeric_cols].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', 
                       center=0, square=True, ax=ax)
            st.pyplot(fig)
    
    with tab3:
        if "Regional Analysis" in viz_type:
            st.subheader("🌐 Regional Distribution")
            if 'WHO Region' in df.columns:
                regional_data = df.groupby('WHO Region')['Confirmed'].sum().sort_values(ascending=False)
                fig = px.pie(values=regional_data.values, 
                            names=regional_data.index,
                            title='COVID-19 Cases by WHO Region')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("📋 Raw Data")
        st.dataframe(top_countries, use_container_width=True)
        
        # Download button
        csv = top_countries.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f'top_{top_n}_countries.csv',
            mime='text/csv'
        )

else:
    st.warning("⚠️ Please upload a COVID-19 dataset to begin analysis.")

# Footer
st.write("---")
st.caption("Dashboard created with Streamlit | Data Visualization Assignment")
