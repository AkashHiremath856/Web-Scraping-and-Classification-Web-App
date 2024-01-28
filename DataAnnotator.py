import pickle
from DataModel import Model 
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import joblib
from sqlalchemy import create_engine
import warnings
import re
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings('ignore')

obj=Model()

class Web_Scrap:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        try:
            raw_data = requests.get(self.url).text
            soup = BeautifulSoup(raw_data, "xml")
            titles = []
            descs = []
            dates = []
            links = []
            for item in soup.find_all("item"):
                title = item.find("title").text if item.find("title") else None
                date = item.find("pubDate").text if item.find("pubDate") else None
                link = item.find("link").text if item.find("link") else None
                desc = item.find("description").text if item.find("description") else None
                pattern = re.compile(r'<p>(.*?)<\/p>', re.DOTALL)
                matches = pattern.findall(desc)
                if matches:
                    cleaned_matches = [re.sub(r'<.*?>', '', match).replace(';','').replace('&','') for match in matches]
                    desc=''
                    for match in cleaned_matches:
                        desc+=''.join(match.strip())
                titles.append(title)
                descs.append(desc)
                dates.append(date)
                links.append(link)
            return titles, descs, dates, links
        except Exception as e:
            print(f"Error Occured: {e}")

    def to_database(self, name: str, df):
        df = df.drop_duplicates(subset='Titles', keep='first')
        df.to_csv(name+'.csv',index=False)
        password=os.environ['password']
        engine = create_engine(f'mysql://root:{password}@localhost:3306/articles')
        try:
            df.to_sql(name, engine, if_exists='replace', index=False, method='multi')
        except Exception as e:
            print(f"Error inserting data: {e}")


    def get_category(self,data_set, model):
        data_set["Titles"] = data_set["Titles"].astype(str)
        data_set["Description"] = data_set["Description"].astype(str)
        loaded_vectorizer = joblib.load('artifacts/vectorizer.joblib')
        X = data_set["Description"].apply(lambda x: obj.preprocess_text(x))
        X = loaded_vectorizer.transform(X)
        proba = np.round(model.predict_proba(X), 2)
        results = []
        for p in proba:
            if np.all(p < 0.6):
                results.append("other")
            else:
                results.append(np.argmax(p))

        value_mapping = {
            0:'disaster',
            1: "political",
            2: "positive",
            3: "protest",
            4: "riot",
            5: "terror",
            "other": "other",
        }
        max_index_mapped = [value_mapping[val] for val in results]
        return max_index_mapped


def main(url,save=False):
    o = Web_Scrap(url)
    titles, descs, dates, links = o.get_data()
    data_set = pd.DataFrame(
        {"Titles": titles, "Description": descs, "Dates": dates, "Links": links}
    )
    if 'model.pkl' not in os.listdir('artifacts/'):
        obj.BuildModel()
    model = pickle.load(open("artifacts/model.pkl", "rb"))
    data_set['Category']=o.get_category(data_set, model)
    if save==True:
        o.to_database('Data1',data_set)
    return data_set