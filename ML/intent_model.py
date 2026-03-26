import pickle

with open("ml/model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

def predict_intent(text):
    X = vectorizer.transform([text])
    return model.predict(X)[0]