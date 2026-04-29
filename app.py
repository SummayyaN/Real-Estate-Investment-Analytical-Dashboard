import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

   
# CONFIG
   
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

   
# LIGHT UI CSS
   
st.markdown("""
<style>
body { background-color: #f8fafc; }
.metric-card {
    background: linear-gradient(135deg, #e0f2fe, #bae6fd);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.metric-title { color: #475569; }
.metric-value { font-size: 28px; font-weight: bold; color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

st.title("Real Estate Investment Analytics Dashboard")

   
# LOAD DATA
   
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_real_estate_data.csv")

df = load_data()

   
# SIDEBAR NAVIGATION
   
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "EDA Analysis", "Project Insights"]
)

   
# SESSION STATE
   
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df.copy()

filtered_df = st.session_state.filtered_df

   
# Overview
   
if page == "Overview":

    st.header("Overview")

    colf1, colf2, colf3 = st.columns(3)

    with colf1:
        city = st.multiselect("City", df["City"].unique())

    with colf2:
        property_type = st.multiselect("Property Type", df["Property_Type"].unique())

    with colf3:
        bhk = st.multiselect("BHK", df["BHK"].unique())

    filtered_df = df.copy()

    if city:
        filtered_df = filtered_df[filtered_df["City"].isin(city)]
    if property_type:
        filtered_df = filtered_df[filtered_df["Property_Type"].isin(property_type)]
    if bhk:
        filtered_df = filtered_df[filtered_df["BHK"].isin(bhk)]

    st.session_state.filtered_df = filtered_df

       
    # KPI CARDS
       
    def card(title, value):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1: card("Total Properties", len(filtered_df))
    with col2: card("Avg Price", round(filtered_df["Price_in_Lakhs"].mean(),2))
    with col3: card("Avg Size", round(filtered_df["Size_in_SqFt"].mean(),2))
    with col4: card("Avg Price/SqFt", round(filtered_df["Price_per_SqFt"].mean(),2))

    st.write("---")

       
    # QUICK INSIGHT CHARTS
       
    st.subheader("Quick Market Insights")

    c1, c2 = st.columns(2)

    # Price Distribution
    with c1:
        fig, ax = plt.subplots()
        ax.hist(filtered_df["Price_in_Lakhs"], bins=25)
        ax.set_title("Price Distribution")
        ax.set_xlabel("Price (Lakhs)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    # Size Distribution
    with c2:
        fig, ax = plt.subplots()
        ax.hist(filtered_df["Size_in_SqFt"], bins=25)
        ax.set_title("Size Distribution")
        ax.set_xlabel("Size (SqFt)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    st.write("---")

       
    # CATEGORY INSIGHTS
       
    c3, c4 = st.columns(2)

    # Properties by City
    with c3:
        st.subheader("Properties by City")
        st.bar_chart(filtered_df["City"].value_counts())

    # Properties by Type
    with c4:
        st.subheader("Property Type Distribution")
        st.bar_chart(filtered_df["Property_Type"].value_counts())

    st.write("---")

       
    # PRICE RELATIONSHIP
       
    st.subheader("Size vs Price Relationship")

    fig, ax = plt.subplots()
    ax.scatter(filtered_df["Size_in_SqFt"], filtered_df["Price_in_Lakhs"])
    ax.set_xlabel("Size (SqFt)")
    ax.set_ylabel("Price (Lakhs)")
    ax.set_title("Size vs Price")
    st.pyplot(fig)

    st.write("---")

       
    # DATA TABLE
       
    st.subheader("Sample Data")
    st.dataframe(filtered_df.head())

   
# EDA PAGE (WITH DROPDOWN)
   
elif page == "EDA Analysis":

    st.header("Exploratory Data Analysis")

    section = st.selectbox(
        "Select Analysis",
        [
            "Price & Size Analysis",
            "Location Analysis",
            "Feature Relationships",
            "Investment Insights"
        ]
    )

    # ----------- 1–5 -----------
    if section == "Price & Size Analysis":

        st.header("1–5 Price & Size Analysis")

        c1, c2 = st.columns(2)

        with c1:
            fig, ax = plt.subplots()
            ax.hist(filtered_df["Price_in_Lakhs"], bins=30)
            ax.set_title("1. Price Distribution", color="blue")
            st.pyplot(fig)

        with c2:
            fig, ax = plt.subplots()
            ax.hist(filtered_df["Size_in_SqFt"], bins=30)
            ax.set_title("2. Size Distribution", color="green")
            st.pyplot(fig)

        c3, c4 = st.columns(2)

        with c3:
            st.bar_chart(filtered_df.groupby("Property_Type")["Price_per_SqFt"].mean())

        with c4:
            fig, ax = plt.subplots()
            ax.scatter(filtered_df["Size_in_SqFt"], filtered_df["Price_in_Lakhs"])
            ax.set_title("4. Size vs Price", color="purple")
            st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.boxplot(filtered_df["Price_per_SqFt"])
        ax.set_title("5. Outliers in Price/SqFt", color="red")
        st.pyplot(fig)

    # ----------- 6–10 -----------
    elif section == "Location Analysis":

        st.header("6–10 Location Analysis")

        c1, c2 = st.columns(2)

        with c1:
            st.bar_chart(filtered_df.groupby("State")["Price_per_SqFt"].mean())

        with c2:
            st.bar_chart(filtered_df.groupby("City")["Price_in_Lakhs"].mean())

        c3, c4 = st.columns(2)

        with c3:
            st.bar_chart(filtered_df.groupby("Locality")["Age_of_Property"].median())

        with c4:
            st.bar_chart(filtered_df["BHK"].value_counts())

        top5 = filtered_df.groupby("Locality")["Price_in_Lakhs"].mean().nlargest(5)
        st.bar_chart(top5)

    # ----------- 11–15 -----------
    elif section == "Feature Relationships":

        st.header("11–15 Feature Relationships")

        c1, c2 = st.columns(2)

        with c1:
            fig, ax = plt.subplots()
            corr = filtered_df.corr(numeric_only=True)
            im = ax.imshow(corr)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticklabels(corr.columns)
            st.pyplot(fig)

        with c2:
            fig, ax = plt.subplots()
            ax.scatter(filtered_df["Nearby_Schools"], filtered_df["Price_per_SqFt"])
            st.pyplot(fig)

        c3, c4 = st.columns(2)

        with c3:
            fig, ax = plt.subplots()
            ax.scatter(filtered_df["Nearby_Hospitals"], filtered_df["Price_per_SqFt"])
            st.pyplot(fig)

        with c4:
            st.bar_chart(filtered_df.groupby("Furnished_Status")["Price_in_Lakhs"].mean())

        st.bar_chart(filtered_df.groupby("Facing")["Price_per_SqFt"].mean())

    # ----------- 16–20 -----------
    elif section == "Investment Insights":

        st.header("16–20 Investment Analysis")

        c1, c2 = st.columns(2)

        with c1:
            st.bar_chart(filtered_df["Owner_Type"].value_counts())

        with c2:
            st.bar_chart(filtered_df["Availability_Status"].value_counts())

        c3, c4 = st.columns(2)

        with c3:
            st.bar_chart(filtered_df.groupby("Parking_Space")["Price_in_Lakhs"].mean())

        with c4:
            st.bar_chart(filtered_df.groupby("Amenities")["Price_per_SqFt"].mean())

        fig, ax = plt.subplots()
        ax.scatter(filtered_df["Public_Transport_Accessibility"], filtered_df["Price_per_SqFt"])
        st.pyplot(fig)

   
# Project Insights
   
if page == "Project Insights":

    st.header("Project Overview & Key Insights")

    st.markdown("Project Objective")
    st.write("""
    This project aims to analyze real estate data to help investors make informed decisions.
    
    It focuses on:
    - Understanding property price trends
    - Identifying high-return investment areas
    - Analyzing factors affecting property valuation
    """)

    st.markdown("Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Total Cities", df["City"].nunique())
    col3.metric("Property Types", df["Property_Type"].nunique())

    st.write("---")

    st.markdown("Key Insights")

       
    # Insight 1: Price Trends
       
    st.markdown("Price Trends")

    avg_price_city = df.groupby("City")["Price_in_Lakhs"].mean().sort_values(ascending=False)
    st.write(f"• Highest average prices observed in: **{avg_price_city.index[0]}**")

    st.bar_chart(avg_price_city.head(10))

       
    # Insight 2: Size vs Price
       
    st.markdown("Size vs Price")

    corr = df["Size_in_SqFt"].corr(df["Price_in_Lakhs"])
    st.write(f"• Strong relationship between size and price (Correlation: **{round(corr,2)}**)")

    fig, ax = plt.subplots()
    ax.scatter(df["Size_in_SqFt"], df["Price_in_Lakhs"])
    ax.set_xlabel("Size (SqFt)")
    ax.set_ylabel("Price (Lakhs)")
    ax.set_title("Size vs Price Relationship")
    st.pyplot(fig)

       
    # Insight 3: Location Impact
       
    st.markdown("Location Impact")

    st.write("• Metro cities show significantly higher price per sq.ft compared to smaller cities")

    state_price = df.groupby("State")["Price_per_SqFt"].mean()
    st.bar_chart(state_price)

       
    # Insight 4: Property Type
       
    st.markdown("Property Type")

    st.write("• Villas and independent houses tend to have higher overall prices")

    type_price = df.groupby("Property_Type")["Price_in_Lakhs"].mean()
    st.bar_chart(type_price)

       
    # Insight 5: Accessibility
       
    st.markdown("Accessibility")

    st.write("• Properties with better transport access show higher valuation")

    fig, ax = plt.subplots()
    ax.scatter(df["Public_Transport_Accessibility"], df["Price_per_SqFt"])
    ax.set_xlabel("Transport Accessibility")
    ax.set_ylabel("Price per SqFt")
    ax.set_title("Transport vs Price")
    st.pyplot(fig)

    st.write("---")

       
    # Business Impact
       
    st.markdown("Business Impact")

    st.write("""
    1. Helps investors identify profitable properties  
    2. Supports real estate companies in pricing strategies  
    Improves decision-making using data-driven insights  
    """)

    st.write("---")

       
    # Conclusion
       
    st.markdown("Conclusion")

    st.write("""
    This dashboard demonstrates how data analytics can transform real estate investment decisions.
    
    By combining multiple factors like location, amenities, and infrastructure,
    investors can make smarter and more profitable choices.
    """)