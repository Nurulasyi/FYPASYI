# password_checker/import_data.py
import pandas as pd
from password_checker.models import PasswordData

def import_dataset(file_path):
    # Baca dataset menggunakan pandas
    dataset = pd.read_csv(file_path)

    # Iterasi melalui baris dataset dan simpan ke model Django
    for index, row in dataset.iterrows():
        password = row['password']
        strength = row['strength']
        PasswordData.objects.create(password=password, strength=strength)

# Panggil fungsi import_dataset dengan memberikan path ke dataset
import_dataset('dataset/data.csv')
