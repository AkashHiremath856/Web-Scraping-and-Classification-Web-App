import streamlit as st
from DataAnnotator import main

st.title('Web Scrap')

option=st.sidebar.radio('URL Input',['URL','Input'])
if option=='URL':
    url=st.selectbox('Select link', [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
    ])
    save=st.checkbox('Save Data into DB',key='url')
    btn= st.button('Scrap')

    if btn and url:
        if save:
            try:
                df=main(url,True)
                st.sidebar.write(df['Category'].value_counts())
                st.dataframe(df)
            except:
                st.write('Try another URL')
        else:
            try:
                df=main(url)
                st.sidebar.write(df['Category'].value_counts())
                st.dataframe(df)
            except:
                st.write('Try another URL')
        

if option=='Input':
    user_input=st.text_input('Enter URL')
    save=st.checkbox('Save Data into DB',key='input')
    btn= st.button('Scrap')
    if btn and user_input:
        if save:
            try:
                df=main(user_input,True)
                st.sidebar.write(df['Category'].value_counts())
                st.dataframe(df)
            except:
                st.write('Try another URL')
        else:
            try:
                df=main(user_input)
                st.sidebar.write(df['Category'].value_counts())
                st.dataframe(df)
            except:
                st.write('Try another URL')
        