
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

# Set Page Configuration
st.set_page_config(
    layout="wide",
    page_title="Enhanced Sales Dashboard 📊",
    page_icon="📈"
)

# Load Dataset
df = pd.read_csv('clean_cafe_sales.csv')

# Page Title
st.title("Enhanced Sales Dashboard 📊")
st.markdown("Gain insights into sales performance using interactive visualizations and key metrics.")

# KPIs Section
st.markdown("### Key Performance Indicators (KPIs)")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    total_sales = df["Total Spent"].sum()
    st.metric("Total Sales", f"${total_sales:,.2f}")

with kpi_col2:
    avg_transaction = df["Total Spent"].mean()
    st.metric("Average Transaction", f"${avg_transaction:,.2f}")

with kpi_col3:
    unique_items = df["Item"].nunique()
    st.metric("Unique Items Sold", unique_items)

with kpi_col4:
    top_item = df.groupby("Item")["Total Spent"].sum().idxmax()
    st.metric("Top-Selling Item", top_item)

# Tabs
tab1, tab2 = st.tabs(["📈 Descriptive Stats", "📊 Charts"])

# Descriptive Statistics Tab
with tab1:
    # Sidebar Toggle for Showing Dataset
  show_data = st.sidebar.checkbox("Show Dataset", False)  # Create a checkbox in the sidebar to show the dataset

if show_data:
    st.markdown("<h3 style='text-align: center; color: LightBlue;'>Dataset</h3>", unsafe_allow_html=True)  # Display a title for the dataset
    st.dataframe(df, height=400)  # Display the first 100 rows of the dataset in a table with a specified height

# Columns for Numerical and Categorical Stats
col1, col2, col3 = st.columns([6, 0.5, 6])  # Create three columns with specified width ratios
with col1:
    st.subheader("Numerical Descriptive Statistics")  # Add a subheader for numerical statistics
    st.dataframe(df.describe().T)  # Display the numerical descriptive statistics transposed

with col3:
    st.subheader("Categorical Descriptive Statistics")  # Add a subheader for categorical statistics
    st.dataframe(df.describe(include='O').T)  # Display the categorical descriptive statistics transposed

# Charts Tab
with tab2:
    # Sidebar Filters
    selected_item = st.sidebar.multiselect("Select Item(s):", options=df['Item'].unique(), default=df['Item'].unique())  # Multi-select filter for items
    selected_location = st.sidebar.multiselect("Select Location(s):", options=df['Location'].unique(), default=df['Location'].unique())  # Multi-select filter for locations
    selected_payment = st.sidebar.multiselect("Select Payment Method(s):", options=df['Payment Method'].unique(), default=df['Payment Method'].unique())  # Multi-select filter for payment methods

    # Filtered DataFrame
    filtered_df = df[
        (df['Item'].isin(selected_item)) &  # Filter dataset by selected items
        (df['Location'].isin(selected_location)) &  # Filter dataset by selected locations
        (df['Payment Method'].isin(selected_payment))  # Filter dataset by selected payment methods
    ]

    # Visualization Columns
    col1, col2, col3 = st.columns([5, 1, 5])  # Create three columns for displaying charts

    # Left Column Charts
    with col1:
        fig1 = px.bar(
            filtered_df, x="Month Name", y="Total Spent", color="Item",  # Create a bar chart for monthly sales by item
            title="Monthly Sales by Item"  # Set the chart title
        )
        st.plotly_chart(fig1, use_container_width=True)  # Display the bar chart

        fig2 = px.scatter(
            filtered_df, x="Transaction Date", y="Total Spent", color="Item",  # Create a scatter plot for sales over time
            size="Total Spent",  # Set size based on total spent
            title="Sales Over Time (Scatter Plot)",  # Set the chart title
            opacity=0.7  # Set the opacity of the scatter points
        )
        st.plotly_chart(fig2, use_container_width=True)  # Display the scatter plot

        fig3 = px.box(
            filtered_df, x="Year", y="Total Spent", color="Item",  # Create a box plot for yearly sales distribution by item
            title="Yearly Sales Distribution"  # Set the chart title
        )
        st.plotly_chart(fig3, use_container_width=True)  # Display the box plot

    # Right Column Charts
    with col3:
        fig4 = px.pie(
            filtered_df, names="Item", values="Total Spent",  # Create a pie chart for sales distribution by item
            title="Sales Distribution by Item"  # Set the chart title
        )
        st.plotly_chart(fig4, use_container_width=True)  # Display the pie chart

        fig5 = px.histogram(
            filtered_df, x="Day", color="Item",  # Create a histogram for sales distribution by day
            title="Sales Distribution by Day",  # Set the chart title
            barmode="group"  # Set the bar mode to 'group' for side-by-side bars
        )
        st.plotly_chart(fig5, use_container_width=True)  # Display the histogram

        fig6 = px.scatter_matrix(
            filtered_df, dimensions=["Total Spent", "Quantity", "Price Per Unit"],  # Create a scatter matrix for multiple dimensions
            color="Item",  # Color by item
            title="Scatter Matrix of Sales Data"  # Set the chart title
        )
        st.plotly_chart(fig6, use_container_width=True)  # Display the scatter matrix
