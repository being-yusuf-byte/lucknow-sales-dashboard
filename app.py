import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Lucknow Sales Dashboard", layout="wide")

# 2. Data Load karna
@st.cache_data
def get_data():
    # Excel file read karna
    df = pd.read_excel("Lucknow_Ecommerce_Sales.xlsx")
    # Date ko sahi format mein convert karna
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = get_data()

    # 3. Sidebar Filters
    st.sidebar.header("Filter Options")
    area = st.sidebar.multiselect(
        "Area Select Karein:",
        options=df["Customer_Area"].unique(),
        default=df["Customer_Area"].unique()
    )
    
    df_selection = df.query("Customer_Area == @area")

    # 4. Main Page UI
    st.title("🛍️ Lucknow E-Commerce Live Dashboard")
    st.markdown("##")

    # Metrics calculate karna (Sirf numeric column ka sum)
    total_sales = int(df_selection["Total_Amount"].sum())
    average_sale = round(df_selection["Total_Amount"].mean(), 2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Revenue", f"₹{total_sales:,}")
    with col2:
        st.metric("Average Order Value", f"₹{average_sale}")

    st.markdown("---")

    # 5. Charts
    left_column, right_column = st.columns(2)

    with left_column:
        # Product wise sales (Numeric only sum)
        sales_by_product = df_selection.groupby("Product_Name")[["Total_Amount"]].sum().sort_values("Total_Amount")
        fig_product = px.bar(
            sales_by_product,
            x="Total_Amount",
            y=sales_by_product.index,
            orientation="h",
            title="<b>Revenue by Product</b>",
            color_discrete_sequence=["#0083B8"]
        )
        st.plotly_chart(fig_product, use_container_width=True)

    with right_column:
        # Payment Mode distribution
        fig_payment = px.pie(
            df_selection, 
            values='Total_Amount', 
            names='Payment_Mode', 
            title='<b>Payment Mode Share</b>',
            hole=0.4
        )
        st.plotly_chart(fig_payment, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check karein ki 'Lucknow_Ecommerce_Sales.xlsx' file GitHub par uploaded hai.")
