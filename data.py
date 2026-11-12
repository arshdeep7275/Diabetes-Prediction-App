
from pathlib import Path
import pandas as pd
import requests, io

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOCAL = DATA_DIR / "diabetes.csv"
URLS = [
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
]
EXPECTED = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"]

def _normalise(df):
    cols = {str(c).strip().lower().replace(" ","_"): c for c in df.columns}
    mapping = {}
    aliases = {
        "pregnancies":["pregnancies","pregnancy"],
        "glucose":["glucose","glucose_level"],
        "bloodpressure":["bloodpressure","blood_pressure"],
        "skinthickness":["skinthickness","skin_thickness"],
        "insulin":["insulin"],
        "bmi":["bmi","body_mass_index"],
        "diabetespedigreefunction":["diabetespedigreefunction","diabetes_pedigree_function","pedigree"],
        "age":["age"],
        "outcome":["outcome","diabetes","target","label"]
    }
    for norm, original in cols.items():
        for target, names in aliases.items():
            if norm in names:
                mapping[original] = target
    df = df.rename(columns=mapping)
    if len(df.columns) == 9 and "outcome" not in df.columns:
        df.columns = EXPECTED
    missing = [c for c in [x.lower() for x in EXPECTED] if c not in df.columns.str.lower().tolist()]
    if missing:
        # second pass for exact expected names
        lower = {c.lower(): c for c in df.columns}
        if all(x in lower for x in [c.lower() for c in EXPECTED]):
            df = df.rename(columns={lower[c.lower()]: c.lower() for c in EXPECTED})
        else:
            raise ValueError("CSV must contain the 8 clinical features and an Outcome/target column.")
    # normalize to canonical lower-case names
    df.columns = [str(c).strip().lower().replace(" ","_") for c in df.columns]
    canonical = [c.lower() for c in EXPECTED]
    df = df[[c for c in canonical if c in df.columns]].copy()
    for c in canonical:
        if c not in df.columns:
            raise ValueError(f"Missing required column: {c}")
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=canonical).reset_index(drop=True)
    df["outcome"] = (df["outcome"] > 0).astype(int)
    return df

def load_diabetes_data(uploaded=None):
    if uploaded is not None:
        return _normalise(pd.read_csv(uploaded))
    if LOCAL.exists():
        try:
            return _normalise(pd.read_csv(LOCAL))
        except Exception:
            pass
    for url in URLS:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            df = pd.read_csv(io.BytesIO(r.content), header=None, names=EXPECTED)
            return _normalise(df)
        except Exception:
            continue
    raise RuntimeError("No dataset available. Upload a compatible CSV from the Data page.")
