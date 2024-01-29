import streamlit as st

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.subheader('changelog: `version 0.1.3`', divider='rainbow')
st.markdown('''
            * اضافه کردن نمودارهای اصلی بر مبنای دلار
            * رفع باگهای کوچک''', unsafe_allow_html=False, help=None)
st.subheader('changelog: `version 0.1.2`', divider='rainbow')
st.markdown('''
            * اضافه کردن مقایسه ماهانه
            * رفع باگهای کوچک''', unsafe_allow_html=False, help=None)
st.subheader('changelog: `version 0.1.1`', divider='rainbow')
st.markdown('''
            * اضافه کردن ورک بنچ
            * رفع باگهای کوچک''', unsafe_allow_html=False, help=None)
st.subheader('changelog: `version 0.1.0`', divider='rainbow')
st.markdown('''
            * گزارش ماهانه فروش
            * گزارش تعداد تولید
            * گزارش تعداد فروش
            * درآمدهای عملیاتی و سود''', unsafe_allow_html=False, help=None)