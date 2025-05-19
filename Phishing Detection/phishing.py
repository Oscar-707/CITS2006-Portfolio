import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# ---------- Step 1: Load your dataset ----------
csv_path = "phishing_site_urls.csv"  # Change this to your CSV file path
df = pd.read_csv(csv_path)

# Assuming your CSV columns are named 'URL' and 'Label'
# If the columns are named differently, update accordingly.

# Step 2: Feature Extraction
def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["num_dots"] = url.count('.')
    features["has_ip"] = bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}', url))
    features["has_at"] = '@' in url
    features["num_subdirs"] = url.count('/')
    features["num_parameters"] = url.count('=')
    features["has_suspicious_words"] = int(any(word in url.lower() for word in ['login', 'secure', 'account', 'update', 'verify']))
    features["uses_https"] = int(url.lower().startswith('https'))
    return features

features_df = df["URL"].apply(extract_features).apply(pd.Series)

# ---------- Step 3: Model Training ----------
X = features_df
le = LabelEncoder()
y = le.fit_transform(df["Label"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# ---------- Step 4: Evaluation ----------
y_pred = clf.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ---------- Step 5: Predict New URLs ----------
def predict_url(url):
    feat = extract_features(url)
    feat_df = pd.DataFrame([feat])
    pred = clf.predict(feat_df)[0]
    return le.inverse_transform([pred])[0]

# Example use
example_url = "http://paypal.secure-login.com/verify"
print(f"\nPrediction for example URL '{example_url}': {predict_url(example_url)}")
