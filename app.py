import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Breadfast Operations", layout="wide")

# 2. CSS الاحترافي (الإطار المضيء، الكروت المربعة، والخلفية)
st.markdown("""
    <style>
    .stApp { background: #020617 !important; color: white; }
    .kpi-box { 
        background: #1e293b !important; 
        border: 1px solid #10b981 !important; 
        border-radius: 15px !important; 
        padding: 20px !important; 
        text-align: center !important; 
        box-shadow: 0px 0px 15px rgba(16, 185, 129, 0.3) !important;
        margin-bottom: 20px;
    }
    .kpi-text { color: #10b981 !important; font-size: 24px !important; font-weight: bold; }
    h2, h3 { color: #10b981 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; color:#10b981;">🚀 Breadfast Operations Intelligence</h1>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📥 ارفع ملف الطلبات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Price (EGP)'] = pd.to_numeric(df['Price (EGP)'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Total_Order_Value'] = df['Price (EGP)'] * df['Quantity']
    df['Order_Time'] = pd.to_datetime(df['Order_Time'], format='%H:%M', errors='coerce').dt.time

    # الحسابات كاملة
    stats = {
        "الطلبات": df['Order_ID'].nunique(),
        "الإيرادات": df['Total_Order_Value'].sum(),
        "متوسط الطلب": df['Total_Order_Value'].mean(),
        "ملغاة": (df['Total_Order_Value'] == 0).sum(),
        "ذروة (8-10ص)": ((df['Order_Time'] >= pd.to_datetime('08:00').time()) & (df['Order_Time'] <= pd.to_datetime('10:00').time())).sum()
    }

    # عرض الـ 5 KPIs الأساسية بكروت مربعة
    cols = st.columns(5)
    for i, (k, v) in enumerate(stats.items()):
        cols[i].markdown(f'<div class="kpi-box"><div>{k}</div><div class="kpi-text">{v:,.0f}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # 3. التحليلات الكاملة (الـ 10 أسئلة والـ Insights)
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

    # 4. زر عرض الداتا الخام
    if st.checkbox("🔍 عرض الداتا الخام"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👋 يرجى رفع ملف البيانات للبدء.")
