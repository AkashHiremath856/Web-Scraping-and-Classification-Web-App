import streamlit as st
from tasks import scrape_url
import time

st.title("Web Scrap")

urls = """http://rss.cnn.com/rss/cnn_topstories.rss,\nhttp://qz.com/feed,\nhttp://feeds.foxnews.com/foxnews/politics,\nhttp://feeds.reuters.com/reuters/businessNews,\nhttp://feeds.feedburner.com/NewshourWorld,\nhttps://feeds.bbci.co.uk/news/world/asia/india/rss.xml"""

url = st.text_area("Enter the urls (with delimiter '`,`')", value=urls)
save = st.checkbox("Save Data into DB", key="url")
btn = st.button("Scrap")

if __name__ == "__main__":
    if btn and url:
        start = time.process_time()
        for u in url.split(","):
            try:
                if save:
                    result = scrape_url.apply_async(args=[u, True])
                else:
                    result = scrape_url.apply_async(args=[u, False])

                s = f"Scraping task is running in the background. Task ID: {result.id}"
                print(s)
            except Exception as e:
                st.write(f"Error: {e}. Try another URL")

        st.text(f"Time taken to scrap{time.process_time()-start}")

# Run celery -A tasks worker --loglevel=INFO
