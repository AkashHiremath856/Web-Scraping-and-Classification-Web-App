import re
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
import pickle
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

nltk.download("punkt")
nltk.download("stopwords")

class Model:
    def __init__(self,limit=1000) -> None:    
        self.LIMIT = limit

    def CreateDataset(self):
        if 'Dataset.csv' not in os.listdir('archives'):
            terror = pd.read_csv("archives/Terrorism.csv", encoding="latin-1")
            terror = terror[["Description"]]
            terror = terror.rename({"Description": "text"}, axis=1)
            terror.dropna(inplace=True)
            terror["category"] = "terror"
            terror = terror.iloc[:self.LIMIT]

            protest = pd.read_csv("archives/Protest.csv", encoding="latin-1")
            def trim(s):
                match = re.search(r":(.*)", s)
                if match:
                    return match.group(1).strip()
                else:
                    return s
                
            protest["text"] = protest["text"].apply(lambda x: trim(x))
            protest = protest[["text"]]
            protest["category"] = "protest"
            protest = protest.iloc[:self.LIMIT]

            political = pd.read_csv("archives/Political.csv",low_memory=False)
            political = political[["text"]]
            political["category"] = "political"
            political = political.iloc[:self.LIMIT]

            riot = pd.read_csv("archives/Riots.csv")
            riot = riot[["text"]]
            riot.dropna(inplace=True)
            riot["category"] = "riot"
            riot = riot.iloc[:self.LIMIT]

            positive = pd.read_csv("archives/Positive.csv")
            positive = positive[["Text"]]
            positive = positive.rename({"Text": "text"}, axis=1)
            positive["category"] = "positive"
            positive = positive.iloc[:self.LIMIT]

            disaster = pd.read_csv("archives/Disaster.csv")
            disaster = disaster[["text"]]
            disaster.dropna(inplace=True)
            disaster["category"] = "disaster"
            disaster = disaster.iloc[:self.LIMIT]

            # Merging Datasets
            df = pd.concat([terror, protest, political, riot, positive, disaster])
            df.sample(n=len(df),random_state=16)
            df.reset_index(drop=True, inplace=True)
            df.to_csv("archives/Dataset.csv", index=False)
    
    
    def preprocess_text(self,text):
        text = text.lower()
        words = word_tokenize(text)
        words = [word for word in words if word.isalpha()]
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word not in stop_words]
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        return " ".join(words)

    def evaluate_model(self,model, X_test, y_test):
        print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

    def BuildModel(self):
        if 'Dataset.csv' not in os.listdir('archives'):
            self.CreateDataset()
        if 'model.pkl' not in os.listdir('artifacts/'):
            df = pd.read_csv("archives/Dataset.csv")
            df["text"] = df["text"].apply(lambda x: self.preprocess_text(str(x)))

            encoder = LabelEncoder()
            encoder.fit(df.category)
            encoder.transform(df.category)
            df["category"] = encoder.fit_transform(df.category)

            X = df["text"]
            y = df["category"]

            vectorizer = CountVectorizer()

            X = vectorizer.fit_transform(X)
            joblib.dump(vectorizer, "artifacts/vectorizer.joblib")

            sampler = RandomUnderSampler()
            X, y = sampler.fit_resample(X, y)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42,stratify=y
            )

            model = MultinomialNB()
            model.fit(X_train, y_train)
            self.evaluate_model(model, X_test, y_test)
            pickle.dump(model, open("artifacts/model.pkl", "wb"))
