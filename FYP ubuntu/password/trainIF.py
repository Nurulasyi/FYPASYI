import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load dataset
data = pd.read_csv("data.csv")  # Ganti nama_file_dataset.csv dengan nama file Anda

# Pisahkan fitur (password) dan target (strength)
X = data['password']
y = data['strength']

# Ubah data string (password) menjadi numerik, misalnya dengan melakukan one-hot encoding atau hashing
# Di sini, saya akan menggunakan one-hot encoding sebagai contoh
X_encoded = pd.get_dummies(X)

# Inisialisasi dan latih model Isolation Forest
model = IsolationForest(contamination=0.1)  # Ubah nilai contamination sesuai kebutuhan
model.fit(X_encoded)

# Simpan model dalam file .pkl
joblib.dump(model, 'model_IF.pkl')
# Misalnya, Anda dapat menggunakan model.predict() untuk mendapatkan prediksi anomali

# Prediksi anomali pada data yang sama
predictions = model.predict(X_encoded)

# Print hasil prediksi
print("Hasil prediksi anomali:")
for password, prediction in zip(X, predictions):
    if prediction == -1:
        print(f"Password: {password} adalah anomali")
    else:
        print(f"Password: {password} adalah normal")




