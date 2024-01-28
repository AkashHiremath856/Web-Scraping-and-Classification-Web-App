import streamlit as st
from tasks import scrape_url

st.title('Web Scrap')

option = st.sidebar.radio('URL Input', ['URL', 'Input'])

if option == 'URL':
    url = st.selectbox('Select link', [
        "http://rss.cnn.com/rss/cnn_topstories.rss",
        "http://qz.com/feed",
        "http://feeds.foxnews.com/foxnews/politics",
        "http://feeds.reuters.com/reuters/businessNews",
        "http://feeds.feedburner.com/NewshourWorld",
        "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
    ])
    save = st.checkbox('Save Data into DB', key='url')
    btn = st.button('Scrap')

    if btn and url:
        if save:
            try:
                result = scrape_url.apply_async(args=[url, True])
                st.text(f"Scraping task is running in the background. Task ID: {result.id}")
                st.sidebar.write(result['Category'].value_counts())
                st.dataframe(result)
            except:
                st.write('Try another URL')
        else:
            try:
                df = scrape_url(url, False)
                st.sidebar.write(df['Category'].value_counts())
                st.dataframe(df)
            except:
                st.write('Try another URL')

if option == 'Input':
    user_input = st.text_input('Enter URL')
    save = st.checkbox('Save Data into DB', key='input')
    btn = st.button('Scrap')
    
    if btn and user_input:
        if save:
            try:
                result = scrape_url.apply_async(args=[user_input, True])
                st.text(f"Scraping task is running in the background. Task ID: {result.id}")
                st.sidebar.write(result['Category'].value_counts())
                st.dataframe(result)
            except Exception as e :
                st.write('Try another URL{e}')
        else:
            try:
                df = scrape_url(user_input, False)
                st.sidebar.write(df['Category'].value_counts())
                st.dataframe(df)
            except:
                st.write('Try another URL')
