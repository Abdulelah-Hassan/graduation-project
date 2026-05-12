# Naive bayes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler          # ← keeps data ≥ 0
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     learning_curve, KFold)
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score,
                             ConfusionMatrixDisplay)

def predictTrust():
    df = pd.read_csv("single_account.csv",
                    encoding="latin1")
    df.columns = df.columns.str.strip()
    df = df[df["binary_label"].isin(["Trusted", "Untrusted"])]
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df["bio_text"] = df["biography"].fillna("")
    df["all_hashtags"] = (df["post_hashtags"].fillna("") + " " +
                        df["bio_hashtags"].fillna("")).str.replace(
                            r'[\[\]\"]', " ", regex=True)
    df["text_features"] = df["bio_text"] + " " + df["all_hashtags"]

    # cast numeric-like columns to real numbers
    for col in ["followers", "following", "posts_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["following"] = df["following"].replace(0, 1)       # avoid ÷0

    # robust TRUE/FALSE → 1/0
    def bool_to_int(series):
        truthy = {"1", "true", "yes", "y", "t"}
        return (series.fillna("0")
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .isin(truthy)
                    .astype(int))

    df["is_verified"]             = bool_to_int(df["is_verified"])
    df["is_professional_account"] = bool_to_int(df["is_professional_account"])
    df["is_business_account"]     = bool_to_int(df["is_business_account"])

    # follower ratio
    df["follower_ratio"] = df["followers"] / df["following"]

    # profile completeness
    comp_cols = ["biography", "profile_image_link",
                "business_email", "external_url"]
    df["profile_completeness"] = df[comp_cols].notna().mean(axis=1)

    # activity score
    df["activity_score"] = df["posts_count"]

    # VAT flag (placeholder until scraper added)
    df["vat_valid"] = 0

    # other validation  – combine several quick checks
    def presence(col):
        return (~df[col].isna() & df[col].astype(str).str.len().gt(0)).astype(int)
    other_checks = [
        df["is_verified"],
        df["is_professional_account"],
        presence("external_url"),
        presence("business_address_json"),
        presence("fbid")
    ]
    df["other_validation"] = np.vstack(other_checks).sum(axis=0)

    BUSINESS_W     = np.array([0.20, 0.20, 0.20, 0.20, 0.20])
    NON_BUSINESS_W = np.array([0.30, 0.25, 0.25, 0.00, 0.20])

    base = df[["follower_ratio", "profile_completeness",
            "activity_score", "vat_valid", "other_validation"]].values
    weights = np.where(df["is_business_account"].values.reshape(-1, 1),
                    BUSINESS_W, NON_BUSINESS_W)

    df["trust_score_formula"] = (base * weights).sum(axis=1)


    text_feat     = "text_features"
    numeric_feats = ["follower_ratio", "profile_completeness",
                    "activity_score", "vat_valid",
                    "other_validation", "trust_score_formula"]

    X = df[[text_feat] + numeric_feats]
    y = df["binary_label"].values

    preprocessor = ColumnTransformer([
            ("txt", TfidfVectorizer(stop_words="english",
                                    max_features=2000), text_feat),
            ("num", Pipeline([("sc", MinMaxScaler())]), numeric_feats)
        ])

    pipe = Pipeline([
            ("prep", preprocessor),
            ("model", BaggingClassifier(estimator=ComplementNB(),
                                        random_state=42))
        ])

    param_grid = {
        "model__n_estimators":        [10, 20, 30],
        "model__max_samples":         [0.6, 0.8, 1.0],
        "model__estimator__alpha":    [0.5, 1.0, 2.0]
    }

    account = X.iloc[[0]]


    best = joblib.load("naive_bayes.pkl")


    pred = best.predict(account)

    return pred

    #print(f"✅ Accuracy : {accuracy_score(y_te, pred)*100:.2f}%")
    #print(f"✅ Precision: {precision_score(y_te, pred, average='weighted')*100:.2f}%")
    #print(f"✅ Recall   : {recall_score(y_te, pred, average='weighted')*100:.2f}%")
    #print(f"✅ F1 Score : {f1_score(y_te, pred, average='weighted')*100:.2f}%")

