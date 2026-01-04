import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import torch
torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Configuration ---
FILE_PATH = r"C:\Users\mahad\Downloads\clickbait_data.csv"
SBERT_MODEL_NAME = 'all-MiniLM-L6-v2'
MODEL_DIR = Path(__file__).parent / "modelsnew"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_FILE = MODEL_DIR / "xgb_clickbait.joblib"
EMB_FILE = MODEL_DIR / "embeddings.npy"
LABEL_FILE = MODEL_DIR / "labels.npy"


def load_data(path):
    df = pd.read_csv(path)
    print(f"data has been loaded")
    return df


def get_sbert(model_name):
    sbert = SentenceTransformer(model_name)
    print(f"SBERT Model '{model_name}' loaded.")
    return sbert


def compute_or_load_embeddings(sbert, df):
    if EMB_FILE.exists() and LABEL_FILE.exists():
        print(f"Loading saved embeddings from {EMB_FILE}")
        X = np.load(EMB_FILE)
        y = np.load(LABEL_FILE)
    else:
        print("embedding sentences...")
        X = sbert.encode(df['headline'].tolist(), show_progress_bar=True)
        y = df['clickbait'].values
        np.save(EMB_FILE, X)
        np.save(LABEL_FILE, y)
        print(f"embeddings saved to {EMB_FILE}")
    return X, y


def train_and_save_model(X, y):
    print("training classifier")
    xgb_model = XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
        n_estimators=100,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    xgb_model.fit(X_train, y_train)
    joblib.dump(xgb_model, MODEL_FILE)
    print(f"Model trained and saved to {MODEL_FILE}")

    # evaluation
    y_pred = xgb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy on Test Set: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))
    return xgb_model


def load_or_train(df):
    sbert = get_sbert(SBERT_MODEL_NAME)
    if MODEL_FILE.exists():
       
        xgb_model = joblib.load(MODEL_FILE)
        return sbert, xgb_model

    
    X, y = compute_or_load_embeddings(sbert, df)
    xgb_model = train_and_save_model(X, y)
    return sbert, xgb_model

df = load_data(FILE_PATH)
sbert, model = load_or_train(df)

def predict_examples(sbert=sbert, model=model, examples=[]):
    emb = sbert.encode(examples)
    preds = model.predict(emb)
    return preds


def clickbait_score(title):
    xnew= [title]
    ynew = predict_examples(sbert, model, xnew)
    return ynew[0]
    



