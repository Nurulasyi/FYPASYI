from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
import pandas as pd

# Load dataset
data = pd.read_csv('pentest.csv')

# Assuming the last column is the label and the rest are features
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Initialize KMeans model with desired number of clusters (K)
kmeans = KMeans(n_clusters=2, random_state=42)

# Fit the model to the data
kmeans.fit(X)

# Predict cluster labels for the data
y_pred = kmeans.predict(X)

# Measure accuracy (for demonstration purposes, as K-Means is not a classification algorithm)
accuracy = accuracy_score(y, y_pred)

print("Accuracy:", accuracy)
