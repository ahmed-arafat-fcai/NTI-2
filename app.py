import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم الاحترافي (Dark UI & Borders)
st.set_page_config(page_title="Breadfast Analytics Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0B0E14; padding: 20px; }
    .metric-card { background-color: #1E293B; border: 1px solid #10B981; border-radius: 12px; padding: 15px; text-align: center; }
    h1, h2 { color: #10B981; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Breadfast Operations Intelligence")
uploaded_file = st.file_uploader("📥 ارفع ملف الطلبات (CSV)", type="csv")

if uploaded_file is not None:
    # معالجة البيانات
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Price (EGP)'] = pd.to_numeric(df['Price (EGP)'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Total_Order_Value'] = df['Price (EGP)'] * df['Quantity']
    df['Order_Time'] = pd.to_datetime(df['Order_Time'], format='%H:%M', errors='coerce').dt.time

    # 2. احتساب الـ 10 نقاط بالكامل
    stats = {
        "إجمالي الطلبات": df['Order_ID'].nunique(),
        "إجمالي الإيرادات": df['Total_Order_Value'].sum(),
        "متوسط قيمة الطلب": df['Total_Order_Value'].mean(),
        "طلبات ملغاة (0 EGP)": (df['Total_Order_Value'] == 0).sum(),
        "طلبات الذروة (8-10ص)": ((df['Order_Time'] >= pd.to_datetime('08:00').time()) & (df['Order_Time'] <= pd.to_datetime('10:00').time())).sum()
    }

    # 3. عرض الـ Metrics في كروت احترافية
    st.subheader("📌 الملخص التنفيذي")
    cols = st.columns(5)
    for i, (k, v) in enumerate(stats.items()):
        cols[i].metric(k, f"{v:,.0f}")

    # 4. الرؤى التحليلية والرسومات
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📈 تحليل الأداء")
        st.write("الإيرادات حسب التصنيف")
        st.bar_chart(df.groupby('Category')['Total_Order_Value'].sum())
        st.write(f"🏆 المنتج الأعلى ربحاً: **{df.groupby('Product')['Total_Order_Value'].sum().idxmax()}**")
        st.write(f"📁 التصنيف الأكثر مبيعاً: **{df.groupby('Category')['Quantity'].sum().idxmax()}**")

    with c2:
        st.subheader("👥 تحليل العملاء والمخزون")
        st.write("المنتجات التي تحتاج إعادة تخزين (أقل من 5 قطع)")
        st.bar_chart(df.groupby('Product')['Quantity'].sum()[df.groupby('Product')['Quantity'].sum() < 5])
        st.write(f"⭐ العميل الأعلى قيمة: **{df.loc[df['Total_Order_Value'].idxmax()]['Customer']}**")
        st.write(f"📉 العميل الأقل قيمة: **{df.loc[df['Total_Order_Value'].idxmin()]['Customer']}**")

    # 5. زر عرض الداتا
    if st.checkbox("🔍 عرض الداتا الخام"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👋 يرجى رفع ملف الـ CSV للبدء في التحليل.")

# ديجرام توضيحي لهيكلة الداشبورد
