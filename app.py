import streamlit as st
import pandas as pd

# 1. إعداد الصفحة وتأثيرات CSS للخلفية والكروت
st.set_page_config(page_title="Breadfast Operations", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%); color: white; }
    div[data-testid="stMetricValue"] { color: #10b981; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Breadfast Operations Dashboard")
uploaded_file = st.file_uploader("ارفع ملف الطلبات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Price (EGP)'] = pd.to_numeric(df['Price (EGP)'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Total_Order_Value'] = df['Price (EGP)'] * df['Quantity']
    
    # 2. الكروت المضيئة (KPIs)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("إجمالي الإيرادات", f"{df['Total_Order_Value'].sum():,.0f} EGP")
    with c2: st.metric("عدد الطلبات", int(df['Order_ID'].nunique()))
    with c3: st.metric("متوسط القيمة", f"{df['Total_Order_Value'].mean():,.0f} EGP")
    with c4: st.metric("طلبات ملغاة", int((df['Total_Order_Value'] == 0).sum()))

    # 3. التحليلات (رسومات مدمجة في Streamlit فقط)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("الإيرادات حسب التصنيف")
        cat_data = df.groupby('Category')['Total_Order_Value'].sum()
        st.bar_chart(cat_data)
        
    with col2:
        st.subheader("كميات المنتجات المتبقية (إعادة التخزين)")
        # فلترة المنتجات القليلة (أقل من 5)
        stock_data = df.groupby('Product')['Quantity'].sum()
        restock_data = stock_data[stock_data < 5]
        st.bar_chart(restock_data)

    # 4. عرض الداتا
    if st.checkbox("عرض الداتا الكاملة"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("يرجى رفع ملف البيانات للبدء.")
