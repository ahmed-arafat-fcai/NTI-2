import streamlit as st
import pandas as pd

st.set_page_config(page_title="Breadfast Operations", layout="wide")
st.title("📊 Breadfast Smart Operations Dashboard")

uploaded_file = st.file_uploader("ارفع ملف الطلبات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Price (EGP)'] = pd.to_numeric(df['Price (EGP)'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Total_Order_Value'] = df['Price (EGP)'] * df['Quantity']
    df['Order_Time'] = pd.to_datetime(df['Order_Time'], format='%H:%M', errors='coerce').dt.time

    # --- الجزء الأول: الـ 10 أسئلة الأساسية ---
    # حسابات الـ KPIs
    rush_hour_mask = (df['Order_Time'] >= pd.to_datetime('08:00').time()) & (df['Order_Time'] <= pd.to_datetime('10:00').time())
    
    st.subheader("📌 الملخص التنفيذي")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي الطلبات", int(df['Order_ID'].nunique()))
    c2.metric("إجمالي الإيرادات", f"{df['Total_Order_Value'].sum():,.0f} EGP")
    c3.metric("متوسط قيمة الطلب", f"{df['Total_Order_Value'].mean():,.0f} EGP")
    c4.metric("طلبات ملغاة", int((df['Total_Order_Value'] == 0).sum()))

    # --- الجزء الثاني: تحليل تفصيلي ---
    col1, col2 = st.columns(2)
    with col1:
        st.write("أعلى المنتجات ربحاً")
        st.bar_chart(df.groupby('Product')['Total_Order_Value'].sum())
    with col2:
        st.write("أكثر التصنيفات مبيعاً (بالكمية)")
        st.bar_chart(df.groupby('Category')['Quantity'].sum())

    # --- الجزء الثالث: 3 إضافات تحليلية (Insights) ---
    st.subheader("💡 رؤى إضافية (Advanced Insights)")
    i1, i2, i3 = st.columns(3)
    
    # 1. قائمة إعادة التخزين (Restocking)
    restock = df.groupby('Product')['Quantity'].sum()
    i1.write("⚠️ منتجات تحتاج إعادة تخزين")
    i1.dataframe(restock[restock < 5], use_container_width=True)
    
    # 2. عملاء النخبة مقابل العملاء الجدد
    i2.write("⭐ عملاء النخبة (Highest Value)")
    i2.success(df.loc[df['Total_Order_Value'].idxmax()]['Customer'])
    i2.write("📉 عملاء بحد أدنى (Lowest Value)")
    i2.info(df.loc[df['Total_Order_Value'].idxmin()]['Customer'])
    
    # 3. ساعات الذروة
    i3.write("⏰ ضغط ساعات الذروة (8-10ص)")
    i3.metric("عدد الطلبات", int(rush_hour_mask.sum()))

else:
    st.info("يرجى رفع ملف البيانات للبدء.")
