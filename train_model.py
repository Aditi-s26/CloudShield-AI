import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Correct NSL-KDD columns
columns = [
    "duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot",
    "num_failed_logins","logged_in","num_compromised","root_shell",
    "su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label",
    "difficulty"
]

print("Loading dataset...")

# Load dataset
df = pd.read_csv(
    "dataset/KDDTrain+.txt",
    names=columns,
    header=None
)

print("\nDataset Loaded Successfully!")
print(df.head())
print("\nDataset Shape:")
print(df.shape)

# Remove difficulty column
df.drop("difficulty", axis=1, inplace=True)

# Simplify attack labels
def simplify_attack(label):

    label = str(label)

    if label == "normal":
        return "normal"

    elif "neptune" in label or "smurf" in label:
        return "dos"

    elif "satan" in label or "ipsweep" in label:
        return "probe"

    elif "guess_passwd" in label:
        return "r2l"

    else:
        return "u2r"

print("\nProcessing labels...")

df["label"] = df["label"].apply(simplify_attack)

# Encode categorical columns
print("Encoding categorical data...")

encoder = LabelEncoder()

for col in ["protocol_type", "service", "flag"]:
    df[col] = encoder.fit_transform(df[col])

# Features and labels
X = df.drop("label", axis=1)
y = df["label"]

print("\nSplitting dataset...")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Random Forest model...")

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("\nTesting model...")

# Accuracy
accuracy = model.score(X_test, y_test)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, "model.pkl")

print("\nModel saved successfully as model.pkl")
print("Training Complete!")