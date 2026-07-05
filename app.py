import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="Breadfast Operations", layout="wide")
st.title("📊 Breadfast Operations Intelligence")

uploaded_file = st.file_uploader("قم برفع ملف الطلبات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # تنظيف بسيط
    df.columns = df.columns.str.strip()
    df['Price (EGP)'] = pd.to_numeric(df['Price (EGP)'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Total_Order_Value'] = df['Price (EGP)'] * df['Quantity']
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الإيرادات", f"{df['Total_Order_Value'].sum():,.0f} EGP")
    c2.metric("عدد الطلبات", int(df['Order_ID'].nunique()))
    c3.metric("متوسط قيمة الطلب", f"{df['Total_Order_Value'].mean():,.0f} EGP")
    
    # رسم بياني مدمج (لا يحتاج مكتبات)
    st.subheader("تحليل الإيرادات حسب التصنيف")
    category_data = df.groupby('Category')['Total_Order_Value'].sum()
    st.bar_chart(category_data)
    
    st.dataframe(df)
else:
    st.info("يرجى رفع ملف البيانات للبدء.")
