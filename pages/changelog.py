"""Page log for changes and new improvement in project."""

import streamlit as st
from menu import add_menu

st.set_page_config(layout='wide',
                   page_title="وسهم - بهبودها",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open("style.css", encoding="utf-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()


st.subheader('changelog: `version 0.1.6`', divider='rainbow')
st.markdown('''
            * اضافه شدن تحلیل مونته کارلو شاخص های مهم
            * اضافه کردن متریک های یک سهم
            * اصلاح پروسه لاگین کاربر
            * عدم خروج کاربر بعد از بازنشانی صفحه
            * رفع باگهای کوچک''', unsafe_allow_html=False, help=None)
st.subheader('changelog: `version 0.1.5`', divider='rainbow')
st.markdown('''
            * اضافه شدن صفحه بررسی عملکرد پورتفو
            * رفع باگهای کوچک''', unsafe_allow_html=False, help=None)
st.subheader('changelog: `version 0.1.4`', divider='rainbow')
st.markdown('''
            * اضافه کردن نمودار پی به ای
            * رفع باگهای کوچک''', unsafe_allow_html=False, help=None)
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
