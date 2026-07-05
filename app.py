import streamlit as st
import pandas as pd

# إعداد الصفحة لتكون واسعة واحترافية
st.set_page_config(page_title="Breadfast Analytics Pro", layout="wide")

st.title("🚀 Breadfast Operations Dashboard")
st.markdown("---")

uploaded_file = st.file_uploader("ارفع ملف الداتا اليومي", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Price (EGP)'] = pd.to_numeric(df['Price (EGP)'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Total_Order_Value'] = df['Price (EGP)'] * df['Quantity']
    df['Order_Time'] = pd.to_datetime(df['Order_Time'], format='%H:%M', errors='coerce').dt.time

    # 1. الصف الأول: الـ KPIs الأساسية
    st.subheader("📊 ملخص الأداء اليومي")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("الإيرادات", f"{df['Total_Order_Value'].sum():,.0f} EGP")
    c2.metric("عدد الطلبات", int(df['Order_ID'].nunique()))
    c3.metric("متوسط الطلب", f"{df['Total_Order_Value'].mean():,.0f} EGP")
    c4.metric("طلبات بقيمة 0", int((df['Total_Order_Value'] == 0).sum()))

    # 2. الصف الثاني: تحليل استراتيجي
    st.markdown("---")
    st.subheader("📈 تحليلات إضافية")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("الإيرادات حسب التصنيف")
        st.bar_chart(df.groupby('Category')['Total_Order_Value'].sum())
        
    with col_b:
        st.write("قائمة إعادة التخزين (أقل من 5 قطع)")
        restock = df.groupby('Product')['Quantity'].sum()
        st.dataframe(restock[restock < 5], use_container_width=True)

    # 3. عرض البيانات الخام بشكل منظم
    with st.expander("اضغط هنا لعرض تفاصيل الداتا الكاملة"):
        st.dataframe(df, use_container_width=True)
else:
    st.warning("يرجى رفع الملف لعرض الداشبورد.")
