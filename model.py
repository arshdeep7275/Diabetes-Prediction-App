
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

FEATURES = ["pregnancies","glucose","bloodpressure","skinthickness","insulin","bmi","diabetespedigreefunction","age"]

def train_model(df):
    X, y = df[FEATURES], df["outcome"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("rf", RandomForestClassifier(
            n_estimators=300, max_depth=8, min_samples_leaf=2,
            class_weight="balanced", random_state=42, n_jobs=-1
        ))
    ])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    prob = pipe.predict_proba(X_test)[:,1]
    metrics = {
        "Accuracy": accuracy_score(y_test,pred),
        "Precision": precision_score(y_test,pred,zero_division=0),
        "Recall": recall_score(y_test,pred,zero_division=0),
        "F1 Score": f1_score(y_test,pred,zero_division=0),
        "ROC-AUC": roc_auc_score(y_test,prob)
    }
    cm = confusion_matrix(y_test,pred)
    importances = pipe.named_steps["rf"].feature_importances_
    importance = pd.DataFrame({"Feature":FEATURES,"Importance":importances}).sort_values("Importance",ascending=False)
    return {"pipeline":pipe,"metrics":metrics,"cm":cm,"importance":importance,"X_test":X_test,"y_test":y_test,"pred":pred,"prob":prob}
