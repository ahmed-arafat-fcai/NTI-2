import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. تعريف الكلاس (المنطق)
class BreadfastAnalytics:
    def __init__(self, df):
        self.df = df.copy()
        self._preprocess()

    def _preprocess(self):
        self.df.columns = self.df.columns.str.strip()
        self.df['Price (EGP)'] = pd.to_numeric(self.df['Price (EGP)'], errors='coerce').fillna(0)
        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'], errors='coerce').fillna(0)
        self.df['Total_Order_Value'] = self.df['Price (EGP)'] * self.df['Quantity']
        self.df['Order_Time'] = pd.to_datetime(self.df['Order_Time'], format='%H:%M', errors='coerce').dt.time

# 2. إعدادات الصفحة
st.set_page_config(page_title="Breadfast Operations", layout="wide")
st.title("📊 Breadfast Operations Intelligence")

uploaded_file = st.file_uploader("قم برفع ملف الطلبات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    analysis = BreadfastAnalytics(df)
    data = analysis.df
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الإيرادات", f"{data['Total_Order_Value'].sum():,.0f} EGP")
    c2.metric("عدد الطلبات", int(data['Order_ID'].nunique()))
    c3.metric("متوسط قيمة الطلب", f"{data['Total_Order_Value'].mean():,.0f} EGP")
    
    # رسم بياني باستخدام streamlit المدمج (لا يحتاج مكتبات إضافية)
    st.subheader("تحليل الإيرادات حسب التصنيف")
    category_data = data.groupby('Category')['Total_Order_Value'].sum()
    st.bar_chart(category_data)
    
    # عرض الجدول
    with st.expander("عرض تفاصيل الطلبات"):
        st.dataframe(data)
else:
    st.info("يرجى رفع ملف البيانات للبدء.")
