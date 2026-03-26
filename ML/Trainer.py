import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# cargar dataset
with open("reminder_bot/ML/data/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [d["text"] for d in data]
labels = [d["label"] for d in data]

# vectorizar
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X = vectorizer.fit_transform(texts)

# modelo
model = MultinomialNB()
model.fit(X, labels)

# guardar modelo
with open("reminder_bot/ML/model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

#vemos las probabilidades de cada clase
probs = model.predict_proba(X)
print(probs)