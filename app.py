import streamlit as st
import pandas as pd

st.set_page_config(page_title="Breadfast Operations", layout="wide")

# --- CSS الاحترافي ---
st.markdown("""
    <style>
    /* خلفية الموقع */
    .stApp { background: #020617; }

    /* عنوان الموقع المضيء */
    .glow-title { 
        text-align: center; color: #fff; font-size: 3rem; 
        text-shadow: 0 0 10px #10B981, 0 0 20px #10B981; 
        border: 2px solid #10B981; border-radius: 10px; padding: 10px;
    }

    /* كروت الملخص التنفيذي */
    .kpi-card { 
        background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; 
        border-radius: 15px; padding: 20px; text-align: center;
        transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #10B981; box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2); }
    
    /* تصميم الـ Metrics */
    div[data-testid="stMetricValue"] { color: #10B981 !important; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# العنوان المضيء
st.markdown('<h1 class="glow-title">🚀 Breadfast Operations Intelligence</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📥 ارفع ملف البيانات", type="csv")

if uploaded_file is not None:
    # (المنطق كما هو بدون تغيير)
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Total_Order_Value'] = pd.to_numeric(df['Price (EGP)']) * pd.to_numeric(df['Quantity'])
    
    # حسابات KPIs (كما هي)
    stats = {
        "إجمالي الطلبات": df['Order_ID'].nunique(),
        "الإيرادات": df['Total_Order_Value'].sum(),
        "متوسط الطلب": df['Total_Order_Value'].mean(),
        "ملغاة": (df['Total_Order_Value'] == 0).sum()
    }

    # عرض كروت الملخص التنفيذي بـ CSS
    st.subheader("📌 الملخص التنفيذي")
    cols = st.columns(4)
    for i, (k, v) in enumerate(stats.items()):
        with cols[i]:
            st.markdown(f'<div class="kpi-card"><h4>{k}</h4><p style="font-size:24px; color:#10B981;">{v:,.0f}</p></div>', unsafe_allow_html=True)

    # الرسوم البيانية (KPIs من تحت)
    st.markdown("---")
    st.subheader("📊 تفاصيل التحليل")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📈 الإيرادات حسب التصنيف")
        st.bar_chart(df.groupby('Category')['Total_Order_Value'].sum())
    with col2:
        st.write("📦 تحليل الكميات")
        st.bar_chart(df.groupby('Product')['Quantity'].sum())
else:
    st.info("يرجى رفع ملف الـ CSV للبدء.")
