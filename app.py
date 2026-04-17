import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from scipy import stats

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
        ["Top 5 Bar Chart", "Top 10 Line Plot", "Top 20 Line Plot", "Active Cases Line", 
         "Pairplot", "Correlation Heatmap", "Regional Bar Chart", "Lollipop Charts", 
         "WHO Region Analysis", "Statistical Analysis"],
        default=["Top 5 Bar Chart", "Top 10 Line Plot", "Correlation Heatmap", "Statistical Analysis"]
    )
    
    # Color palette selector
    color_palette = st.selectbox(
        "Choose Color Palette",
        ["bright", "deep", "muted", "pastel", "dark", "colorblind"]
    )
    
    # Theme selector for Plotly
    st.subheader("🎨 Chart Themes")
    chart_theme = st.selectbox(
        "Select Chart Theme",
        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"]
    )
    
    # Animation toggle
    enable_animations = st.toggle("Enable Animations", value=True)
    
    # Data range selector
    st.subheader("📈 Data Filters")
    if not uploaded_file:
        # Load default data to get ranges
        try:
            temp_df = pd.read_csv('covid_19.csv')
            max_confirmed = int(temp_df['Confirmed'].max())
            confirmed_range = st.slider(
                "Confirmed Cases Range",
                0, max_confirmed,
                (0, max_confirmed),
                step=10000
            )
        except:
            confirmed_range = (0, 10000000)
    
    # Info section
    st.subheader("ℹ️ About")
    st.info("""
    **Interactive COVID-19 Dashboard**
    
    ✨ **Features:**
    - 🎯 Interactive visualizations
    - 🌈 Customizable color themes  
    - 📊 Real-time filtering
    - 📱 Mobile responsive
    - 💾 Data export options
    
    **Tip:** Hover over charts for detailed information!
    """)

# Load Data Function
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # Load default dataset
        df = pd.read_csv('covid_19.csv')
    return df

# Main Dashboard Content
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    # Load default dataset
    try:
        df = load_data(None)
    except FileNotFoundError:
        st.error("❌ COVID-19 dataset not found. Please upload a CSV file.")
        st.stop()
    
    # Display basic statistics in columns
    # Set global template for all Plotly charts
    import plotly.io as pio
    pio.templates.default = chart_theme
    
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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Basic Charts", "📈 Advanced Plots", "🔥 Correlation", "🌐 Regional", "📊 Statistical Analysis", "📋 Data"])
    
    with tab1:
        # Top 5 Countries Bar Chart - Interactive
        if "Top 5 Bar Chart" in viz_type:
            st.subheader("🏆 Top 5 Countries by Confirmed Cases")
            top_5 = df.nlargest(5, 'Confirmed')
            
            # Add animation toggle
            if enable_animations:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=top_5['Country/Region'],
                    y=top_5['Confirmed'],
                    text=top_5['Confirmed'],
                    texttemplate='%{text:,.0f}',
                    textposition='outside',
                    marker=dict(
                        color=top_5['Confirmed'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Cases")
                    ),
                    hovertemplate='<b>%{x}</b><br>Confirmed: %{y:,.0f}<br>' +
                                'Deaths: %{customdata[0]:,.0f}<br>' +
                                'Recovered: %{customdata[1]:,.0f}<br>' +
                                'Active: %{customdata[2]:,.0f}<extra></extra>',
                    customdata=np.column_stack((top_5['Deaths'], top_5['Recovered'], top_5['Active']))
                ))
                fig.update_layout(
                    title='Top 5 Countries by Confirmed Corona-virus Cases',
                    height=500,
                    showlegend=False,
                    xaxis_title="Country",
                    yaxis_title="Confirmed Cases",
                    title_font_size=16,
                    template=chart_theme,
                    transition_duration=500
                )
            else:
                fig = px.bar(
                    top_5, 
                    x='Country/Region', 
                    y='Confirmed',
                    title='Top 5 Countries by Confirmed Corona-virus Cases',
                    color='Confirmed',
                    color_continuous_scale='Viridis',
                    text='Confirmed',
                    hover_data=['Deaths', 'Recovered', 'Active']
                )
                fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                fig.update_layout(
                    height=500,
                    showlegend=False,
                    xaxis_title="Country",
                    yaxis_title="Confirmed Cases",
                    title_font_size=16,
                    coloraxis_colorbar=dict(title="Cases"),
                    template=chart_theme
                )
            st.plotly_chart(fig, width="stretch")
        
        # Top 10 Line Plot - Interactive
        if "Top 10 Line Plot" in viz_type:
            st.subheader("📈 Confirmed COVID Cases - Top 10 Countries")
            top_10 = df.nlargest(10, 'Confirmed')
            
            # Add option to show individual country lines
            show_individual = st.checkbox("Show individual country trends", value=False)
            
            if show_individual:
                fig = go.Figure()
                colors = px.colors.qualitative.Set3[:len(top_10)]
                
                for i, (idx, row) in enumerate(top_10.iterrows()):
                    fig.add_trace(go.Scatter(
                        x=[row['Country/Region']],
                        y=[row['Confirmed']],
                        mode='markers+lines',
                        name=row['Country/Region'],
                        marker=dict(size=12, color=colors[i]),
                        line=dict(width=3, color=colors[i]),
                        hovertemplate=f'<b>{row["Country/Region"]}</b><br>' +
                                    f'Confirmed: {row["Confirmed"]:,.0f}<br>' +
                                    f'Deaths: {row["Deaths"]:,.0f}<br>' +
                                    f'Recovered: {row["Recovered"]:,.0f}<br>' +
                                    f'Active: {row["Active"]:,.0f}<extra></extra>'
                    ))
                
                # Add connecting line
                fig.add_trace(go.Scatter(
                    x=top_10['Country/Region'], 
                    y=top_10['Confirmed'],
                    mode='lines',
                    name='Trend Line',
                    line=dict(width=2, color='red', dash='dash'),
                    showlegend=False
                ))
                
                fig.update_layout(
                    title='Confirmed COVID Cases of Top 10 Countries (Individual Trends)',
                    height=600,
                    xaxis_title="Country",
                    yaxis_title="Confirmed Cases",
                    title_font_size=16,
                    template=chart_theme,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
            else:
                fig = px.line(
                    top_10, 
                    x='Country/Region', 
                    y='Confirmed',
                    title='Confirmed COVID Cases of Top 10 Countries',
                    markers=True,
                    color_discrete_sequence=['#FF6B6B'],
                    hover_data=['Deaths', 'Recovered', 'Active', 'New cases']
                )
                fig.update_traces(
                    line=dict(width=3),
                    marker=dict(size=10, line=dict(width=2, color='white'))
                )
                fig.update_layout(
                    height=500,
                    xaxis_title="Country",
                    yaxis_title="Confirmed Cases",
                    title_font_size=16,
                    xaxis_tickangle=45,
                    template=chart_theme
                )
            st.plotly_chart(fig, width="stretch")
    
    with tab2:
        # Top 20 Line Plot with Multiple Metrics
        if "Top 20 Line Plot" in viz_type:
            st.subheader("📊 Top 20 Countries - Multi-Metric Analysis")
            top20 = df.nlargest(20, 'Confirmed')
            
            # Create subplot with secondary y-axis
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Confirmed Cases', 'Deaths vs Recovered'),
                vertical_spacing=0.1
            )
            
            # First subplot: Confirmed cases
            fig.add_trace(
                go.Scatter(
                    x=top20['Country/Region'], 
                    y=top20['Confirmed'],
                    mode='lines+markers',
                    name='Confirmed',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{x}</b><br>Confirmed: %{y:,.0f}<extra></extra>'
                ), 
                row=1, col=1
            )
            
            # Second subplot: Deaths and Recovered
            fig.add_trace(
                go.Scatter(
                    x=top20['Country/Region'], 
                    y=top20['Deaths'],
                    mode='lines+markers',
                    name='Deaths',
                    line=dict(color='#FF4444', width=2),
                    marker=dict(size=6),
                    hovertemplate='<b>%{x}</b><br>Deaths: %{y:,.0f}<extra></extra>'
                ), 
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=top20['Country/Region'], 
                    y=top20['Recovered'],
                    mode='lines+markers',
                    name='Recovered',
                    line=dict(color='#4CAF50', width=2),
                    marker=dict(size=6),
                    hovertemplate='<b>%{x}</b><br>Recovered: %{y:,.0f}<extra></extra>'
                ), 
                row=2, col=1
            )
            
            fig.update_layout(
                height=700,
                title_text="COVID-19 Multi-Metric Analysis (Top 20 Countries)",
                title_font_size=16,
                showlegend=True
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, width="stretch")
        
        # Active Cases Interactive Bubble Chart
        if "Active Cases Line" in viz_type:
            st.subheader("🔴 Active COVID Cases - Interactive Bubble Chart")
            top_10_active = df.nlargest(15,'Confirmed')
            
            fig = px.scatter(
                top_10_active, 
                x='Country/Region', 
                y='Active',
                size='Confirmed',
                color='WHO Region',
                hover_data=['Deaths', 'Recovered', 'New cases'],
                title='Active COVID Cases with Bubble Size by Total Confirmed',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(marker=dict(line=dict(width=2, color='white')))
            fig.update_layout(
                height=600,
                xaxis_title="Country",
                yaxis_title="Active Cases",
                title_font_size=16,
                xaxis_tickangle=45,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            st.plotly_chart(fig, width="stretch")
        
        # Interactive Pairplot using Plotly
        if "Pairplot" in viz_type:
            st.subheader("🎯 Interactive Correlation Matrix")
            top_20 = df.nlargest(20, 'Confirmed')
            selected_columns = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases']
            
            # Create correlation matrix
            corr_matrix = top_20[selected_columns].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix of COVID-19 Metrics",
                color_continuous_scale='RdBu_r',
                range_color=[-1, 1]
            )
            fig.update_layout(
                height=500,
                title_font_size=16
            )
            st.plotly_chart(fig, width="stretch")
            
            # 3D Scatter Plot
            st.subheader("🌐 3D Scatter Plot")
            fig_3d = px.scatter_3d(
                top_20, 
                x='Confirmed', 
                y='Deaths', 
                z='Recovered',
                color='WHO Region',
                size='Active',
                hover_name='Country/Region',
                title="3D Visualization: Confirmed vs Deaths vs Recovered",
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_3d.update_layout(height=600)
            st.plotly_chart(fig_3d, width="stretch")
        
        # Interactive Lollipop Charts
        if "Lollipop Charts" in viz_type:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🍭 Interactive Lollipop Chart")
                top_10_active = df.nlargest(10, 'Active')
                
                fig = go.Figure()
                
                # Add lollipop stems
                for i, (country, active) in enumerate(zip(top_10_active['Country/Region'], top_10_active['Active'])):
                    fig.add_trace(go.Scatter(
                        x=[i, i], 
                        y=[0, active],
                        mode='lines',
                        line=dict(color='lightblue', width=4),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                
                # Add lollipop heads
                fig.add_trace(go.Scatter(
                    x=list(range(len(top_10_active))), 
                    y=top_10_active['Active'],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color=top_10_active['Active'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Active Cases"),
                        line=dict(width=2, color='white')
                    ),
                    text=top_10_active['Country/Region'],
                    hovertemplate='<b>%{text}</b><br>Active Cases: %{y:,.0f}<extra></extra>',
                    showlegend=False
                ))
                
                fig.update_layout(
                    title="Top 10 Countries by Active Cases",
                    xaxis=dict(
                        tickmode='array',
                        tickvals=list(range(len(top_10_active))),
                        ticktext=top_10_active['Country/Region'],
                        tickangle=45
                    ),
                    yaxis_title="Active Cases",
                    height=500,
                    title_font_size=14
                )
                st.plotly_chart(fig, width="stretch")
            
            with col2:
                st.subheader("🌈 Rainbow Lollipop Chart")
                top_12 = df.nlargest(12, 'Confirmed').sort_values('Confirmed')
                
                # Color mapping for regions
                region_colors = {
                    'Europe': '#FF6B6B', 'Americas': '#4ECDC4', 
                    'Eastern Mediterranean': '#45B7D1', 'South-East Asia': '#96CEB4', 
                    'Africa': '#FFEAA7', 'Western Pacific': '#DDA0DD'
                }
                colors = [region_colors.get(region, '#95A5A6') for region in top_12['WHO Region']]
                
                fig = go.Figure()
                
                # Add horizontal lollipop stems
                for i, (country, confirmed, color) in enumerate(zip(top_12['Country/Region'], top_12['Confirmed'], colors)):
                    fig.add_trace(go.Scatter(
                        x=[0, confirmed], 
                        y=[i, i],
                        mode='lines',
                        line=dict(color=color, width=4),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                
                # Add lollipop heads
                fig.add_trace(go.Scatter(
                    x=top_12['Confirmed'],
                    y=list(range(len(top_12))),
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=colors,
                        line=dict(width=2, color='white')
                    ),
                    text=top_12['Country/Region'],
                    hovertemplate='<b>%{text}</b><br>Confirmed: %{x:,.0f}<extra></extra>',
                    showlegend=False
                ))
                
                fig.update_layout(
                    title="Top 12 Countries by Confirmed Cases",
                    yaxis=dict(
                        tickmode='array',
                        tickvals=list(range(len(top_12))),
                        ticktext=top_12['Country/Region']
                    ),
                    xaxis_title="Confirmed Cases",
                    height=500,
                    title_font_size=14
                )
                st.plotly_chart(fig, width="stretch")
    
    with tab3:
        if "Correlation Heatmap" in viz_type:
            st.subheader("🔥 Interactive COVID-19 Correlation Heatmap")
            numeric_cols = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases',
                           'Deaths / 100 Cases', 'Recovered / 100 Cases', '1 week % increase']
            
            # Filter columns that exist in the dataset
            available_cols = [col for col in numeric_cols if col in df.columns]
            corr = df[available_cols].corr()
            
            # Create interactive heatmap
            fig = px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                title="COVID-19 Correlation Heatmap",
                color_continuous_scale='RdBu_r',
                range_color=[-1, 1],
                labels=dict(color="Correlation")
            )
            fig.update_layout(
                height=600,
                title_font_size=16,
                font_size=12
            )
            fig.update_traces(textfont_size=10)
            st.plotly_chart(fig, width="stretch")
            
            # Add detailed analysis
            col1, col2 = st.columns(2)
            with col1:
                st.info("""
                **Heatmap Guide:**
                - 🔴 Red: Negative correlation
                - 🔵 Blue: Positive correlation
                - Darker colors = stronger correlations
                """)
            
            with col2:
                # Find strongest correlations
                corr_pairs = []
                for i in range(len(corr.columns)):
                    for j in range(i+1, len(corr.columns)):
                        corr_pairs.append({
                            'pair': f"{corr.columns[i]} vs {corr.columns[j]}",
                            'correlation': corr.iloc[i, j]
                        })
                
                strongest = sorted(corr_pairs, key=lambda x: abs(x['correlation']), reverse=True)[:3]
                st.success("**Strongest Correlations:**")
                for pair in strongest:
                    st.write(f"• {pair['pair']}: {pair['correlation']:.2f}")
            
            # Interactive scatter plots for top correlations
            st.subheader("🎯 Correlation Scatter Plots")
            if len(strongest) > 0:
                top_corr = strongest[0]
                vars = top_corr['pair'].split(' vs ')
                if len(vars) == 2 and vars[0] in df.columns and vars[1] in df.columns:
                    fig_scatter = px.scatter(
                        df.nlargest(30, 'Confirmed'), 
                        x=vars[0], 
                        y=vars[1],
                        color='WHO Region',
                        size='Confirmed',
                        hover_name='Country/Region',
                        title=f"Scatter Plot: {vars[0]} vs {vars[1]} (Top 30 Countries)",
                        trendline="ols",
                        trendline_color_override="red"
                    )
                    fig_scatter.update_layout(
                        height=500,
                        annotations=[
                            dict(
                                x=0.05, y=0.95,
                                xref="paper", yref="paper",
                                text=f"Correlation: {top_corr['correlation']:.3f}",
                                showarrow=False,
                                bgcolor="rgba(255,255,255,0.8)",
                                bordercolor="black",
                                borderwidth=1
                            )
                        ]
                    )
                    st.plotly_chart(fig_scatter, width="stretch")
                    
                    # Display trendline equation and R²
                    import plotly.express as px
                    if hasattr(fig_scatter, 'data') and len(fig_scatter.data) > 1:
                        # Get the trendline data
                        for trace in fig_scatter.data:
                            if trace.mode == 'lines':
                                st.info(f"📈 **Trendline Analysis**: Linear regression shows the relationship between {vars[0]} and {vars[1]}")
                                break
    
    with tab4:
        if "Regional Bar Chart" in viz_type or "WHO Region Analysis" in viz_type:
            st.subheader("🌐 Interactive WHO Regional Analysis")
            
            # Regional comparison with multiple metrics
            if "Regional Bar Chart" in viz_type:
                st.subheader("📊 Regional Comparison Dashboard")
                
                # Create regional summary
                regional_summary = df.groupby('WHO Region').agg({
                    'Confirmed': 'sum',
                    'Deaths': 'sum',
                    'Recovered': 'sum',
                    'Active': 'sum',
                    'New cases': 'sum'
                }).reset_index()
                
                # Multi-metric bar chart
                fig = go.Figure()
                
                metrics = ['Confirmed', 'Deaths', 'Recovered', 'Active']
                colors = ['#FF6B6B', '#FF4444', '#4CAF50', '#FFA726']
                
                for i, metric in enumerate(metrics):
                    fig.add_trace(go.Bar(
                        name=metric,
                        x=regional_summary['WHO Region'],
                        y=regional_summary[metric],
                        marker_color=colors[i],
                        hovertemplate=f'<b>%{{x}}</b><br>{metric}: %{{y:,.0f}}<extra></extra>'
                    ))
                
                fig.update_layout(
                    title="COVID-19 Cases by WHO Region (All Metrics)",
                    xaxis_title="WHO Region",
                    yaxis_title="Number of Cases",
                    barmode='group',
                    height=500,
                    title_font_size=16,
                    xaxis_tickangle=45
                )
                st.plotly_chart(fig, width="stretch")
                
                # Top countries by region
                st.subheader("🏆 Top Countries by Region")
                top_12 = df.nlargest(12, 'Confirmed')
                
                fig_region = px.bar(
                    top_12, 
                    y='Country/Region', 
                    x='Confirmed',
                    color='WHO Region',
                    title='Top 12 Countries by Confirmed Cases (Colored by WHO Region)',
                    orientation='h',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hover_data=['Deaths', 'Recovered', 'Active']
                )
                fig_region.update_layout(
                    height=600,
                    yaxis={'categoryorder':'total ascending'},
                    title_font_size=16
                )
                st.plotly_chart(fig_region, width="stretch")
            
            # Interactive pie charts and treemap
            if "WHO Region Analysis" in viz_type and 'WHO Region' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Enhanced pie chart
                    regional_data = df.groupby('WHO Region')['Confirmed'].sum().sort_values(ascending=False)
                    fig_pie = px.pie(
                        values=regional_data.values, 
                        names=regional_data.index,
                        title='COVID-19 Cases Distribution by WHO Region',
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        hover_data=[regional_data.values]
                    )
                    fig_pie.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>Cases: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
                    )
                    fig_pie.update_layout(height=400)
                    st.plotly_chart(fig_pie, width="stretch")
                
                with col2:
                    # Treemap visualization
                    fig_tree = px.treemap(
                        df.nlargest(20, 'Confirmed'),
                        path=['WHO Region', 'Country/Region'],
                        values='Confirmed',
                        title='Hierarchical View: WHO Regions & Countries',
                        color='Deaths',
                        color_continuous_scale='Reds'
                    )
                    fig_tree.update_layout(height=400)
                    st.plotly_chart(fig_tree, width="stretch")
                
                # Sunburst chart
                st.subheader("☀️ Sunburst Chart - Regional Breakdown")
                fig_sun = px.sunburst(
                    df.nlargest(25, 'Confirmed'),
                    path=['WHO Region', 'Country/Region'],
                    values='Confirmed',
                    title='COVID-19 Cases - Sunburst Visualization',
                    color='Active',
                    color_continuous_scale='Viridis'
                )
                fig_sun.update_layout(height=600)
                st.plotly_chart(fig_sun, width="stretch")
    
    with tab5:
        st.subheader("📊 Advanced Statistical Analysis")
        
        # Regression Analysis Section
        st.subheader("📈 Regression Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            x_var = st.selectbox("Select X Variable", 
                               [col for col in df.select_dtypes(include=[np.number]).columns if col != 'Country/Region'],
                               index=0)
        with col2:
            y_var = st.selectbox("Select Y Variable", 
                               [col for col in df.select_dtypes(include=[np.number]).columns if col != 'Country/Region'],
                               index=1)
        
        if x_var and y_var and x_var != y_var:
            # Multiple regression analysis options
            regression_type = st.radio("Select Regression Type", 
                                     ["Linear (OLS)", "Exponential", "Logarithmic"])
            
            top_countries_stats = df.nlargest(30, 'Confirmed')
            
            if regression_type == "Linear (OLS)":
                fig_reg = px.scatter(
                    top_countries_stats, 
                    x=x_var, 
                    y=y_var,
                    color='WHO Region',
                    size='Confirmed',
                    hover_name='Country/Region',
                    title=f"Linear Regression: {x_var} vs {y_var}",
                    trendline="ols",
                    trendline_color_override="red"
                )
            elif regression_type == "Exponential":
                # Create exponential trendline manually
                fig_reg = px.scatter(
                    top_countries_stats, 
                    x=x_var, 
                    y=y_var,
                    color='WHO Region',
                    size='Confirmed',
                    hover_name='Country/Region',
                    title=f"Exponential Trend: {x_var} vs {y_var}",
                    log_y=True
                )
            else:  # Logarithmic
                fig_reg = px.scatter(
                    top_countries_stats, 
                    x=x_var, 
                    y=y_var,
                    color='WHO Region',
                    size='Confirmed',
                    hover_name='Country/Region',
                    title=f"Logarithmic Trend: {x_var} vs {y_var}",
                    log_x=True
                )
            
            fig_reg.update_layout(height=500)
            st.plotly_chart(fig_reg, width="stretch")
            
            # Statistical Summary
            st.subheader("📊 Statistical Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                correlation = top_countries_stats[x_var].corr(top_countries_stats[y_var])
                st.metric("Correlation Coefficient", f"{correlation:.4f}")
                
            with col2:
                # Calculate R-squared for linear regression
                from scipy import stats
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    top_countries_stats[x_var].fillna(0), 
                    top_countries_stats[y_var].fillna(0)
                )
                st.metric("R-squared", f"{r_value**2:.4f}")
                
            with col3:
                st.metric("P-value", f"{p_value:.4e}")
            
            # Interpretation
            if abs(correlation) > 0.7:
                strength = "Strong"
                color = "🔴" if correlation > 0 else "🔵"
            elif abs(correlation) > 0.4:
                strength = "Moderate" 
                color = "🟠" if correlation > 0 else "🟣"
            else:
                strength = "Weak"
                color = "🟡"
                
            direction = "positive" if correlation > 0 else "negative"
            st.info(f"{color} **{strength} {direction} correlation** detected between {x_var} and {y_var}")
        
        # Distribution Analysis
        st.subheader("📊 Distribution Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            dist_var = st.selectbox("Select Variable for Distribution Analysis", 
                                  [col for col in df.select_dtypes(include=[np.number]).columns])
        
        with col2:
            transform = st.selectbox("Apply Transformation", ["None", "Log", "Square Root", "Square"])
        
        if dist_var:
            data_to_plot = df[dist_var].dropna()
            
            if transform == "Log":
                data_to_plot = np.log(data_to_plot + 1)  # +1 to handle zeros
                title_suffix = " (Log Transformed)"
            elif transform == "Square Root":
                data_to_plot = np.sqrt(data_to_plot)
                title_suffix = " (Square Root Transformed)"
            elif transform == "Square":
                data_to_plot = np.square(data_to_plot)
                title_suffix = " (Squared)"
            else:
                title_suffix = ""
            
            # Create distribution plot
            fig_dist = px.histogram(
                x=data_to_plot,
                nbins=30,
                title=f"Distribution of {dist_var}{title_suffix}",
                marginal="box",
                color_discrete_sequence=['#FF6B6B']
            )
            fig_dist.update_layout(height=400)
            st.plotly_chart(fig_dist, width="stretch")
            
            # Statistical tests
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean", f"{data_to_plot.mean():.2f}")
            with col2:
                st.metric("Median", f"{data_to_plot.median():.2f}")
            with col3:
                st.metric("Std Dev", f"{data_to_plot.std():.2f}")
    
    with tab6:
        st.subheader("📋 Interactive Data Explorer")
        
        # Add filtering options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Region filter
            regions = ['All'] + list(df['WHO Region'].unique()) if 'WHO Region' in df.columns else ['All']
            selected_region = st.selectbox("Filter by WHO Region", regions)
        
        with col2:
            # Minimum cases filter
            min_cases = st.number_input("Minimum Confirmed Cases", min_value=0, value=0, step=1000)
        
        with col3:
            # Sort by options
            sort_options = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases']
            available_sort = [col for col in sort_options if col in df.columns]
            sort_by = st.selectbox("Sort by", available_sort, index=0)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_region != 'All' and 'WHO Region' in df.columns:
            filtered_df = filtered_df[filtered_df['WHO Region'] == selected_region]
        
        filtered_df = filtered_df[filtered_df['Confirmed'] >= min_cases]
        filtered_df = filtered_df.sort_values(sort_by, ascending=False)
        
        # Display filtered data
        st.write(f"**Showing {len(filtered_df)} countries/regions**")
        
        # Interactive table with styling
        def highlight_max(s):
            is_max = s == s.max()
            return ['background-color: #FFE5E5' if v else '' for v in is_max]
        
        # Apply styling to numeric columns only
        numeric_columns = filtered_df.select_dtypes(include=[np.number]).columns
        styled_df = filtered_df.style.apply(highlight_max, subset=numeric_columns)
        
        st.dataframe(styled_df, width="stretch", height=400)
        
        # Summary statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Summary Statistics")
            summary_stats = filtered_df[numeric_columns].describe()
            st.dataframe(summary_stats, width="stretch")
        
        with col2:
            st.subheader("🎯 Key Insights")
            if len(filtered_df) > 0:
                max_confirmed = filtered_df.loc[filtered_df['Confirmed'].idxmax()]
                max_deaths = filtered_df.loc[filtered_df['Deaths'].idxmax()]
                max_recovered = filtered_df.loc[filtered_df['Recovered'].idxmax()]
                
                st.write(f"🔴 **Highest Confirmed Cases:** {max_confirmed['Country/Region']} ({max_confirmed['Confirmed']:,.0f})")
                st.write(f"⚫ **Highest Deaths:** {max_deaths['Country/Region']} ({max_deaths['Deaths']:,.0f})")
                st.write(f"🟢 **Highest Recovered:** {max_recovered['Country/Region']} ({max_recovered['Recovered']:,.0f})")
                
                if 'Deaths / 100 Cases' in filtered_df.columns:
                    avg_mortality = filtered_df['Deaths / 100 Cases'].mean()
                    st.write(f"💀 **Average Mortality Rate:** {avg_mortality:.2f}%")
                
                if 'Recovered / 100 Cases' in filtered_df.columns:
                    avg_recovery = filtered_df['Recovered / 100 Cases'].mean()
                    st.write(f"💚 **Average Recovery Rate:** {avg_recovery:.2f}%")
        
        # Download options
        st.subheader("📥 Download Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download filtered data
            csv_filtered = filtered_df.to_csv(index=False)
            st.download_button(
                label="� Download Filtered Data",
                data=csv_filtered,
                file_name=f'covid_filtered_{selected_region}_{len(filtered_df)}_countries.csv',
                mime='text/csv'
            )
        
        with col2:
            # Download top N
            top_n_download = st.slider("Top N countries to download", 5, min(50, len(filtered_df)), top_n)
            top_data = filtered_df.head(top_n_download)
            csv_top = top_data.to_csv(index=False)
            st.download_button(
                label=f"🏆 Download Top {top_n_download}",
                data=csv_top,
                file_name=f'covid_top_{top_n_download}_countries.csv',
                mime='text/csv'
            )
        
        with col3:
            # Download summary statistics
            csv_summary = summary_stats.to_csv()
            st.download_button(
                label="📈 Download Summary Stats",
                data=csv_summary,
                file_name='covid_summary_statistics.csv',
                mime='text/csv'
            )

# Footer
st.write("---")
st.caption("Dashboard created with Streamlit | Data Visualization Assignment")
    