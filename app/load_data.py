# load_data.py
import pandas as pd
import requests
import json
import time

# Veri seti yolu
data_path = "data/taxi_trips.csv"

# Örnek veriyi yükle
df = pd.read_csv(data_path)

# Önce kayıt olun
register_url = "http://localhost:8000/register"
register_data = {
    "username": "admin",
    "password": "admin123",
    "email": "admin@example.com"
}
response = requests.post(register_url, json=register_data)
print("Kayıt yanıtı:", response.status_code, response.text)

# Giriş yapıp token alın
login_url = "http://localhost:8000/login"
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(login_url, data=login_data)
token_data = response.json()
token = token_data["access_token"]
print(f"Token alındı: {token}")

# Veri girişi için API endpoint'i
trips_url = "http://localhost:8000/trips"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# İlk 5 kaydı API'ye gönder
for i, row in df.head(5).iterrows():
    # Kayıt verilerini API'nin beklediği formata dönüştür
    trip_data = {
        "VendorID": int(row["VendorID"]),
        "tpep_pickup_datetime": row["tpep_pickup_datetime"],
        "tpep_dropoff_datetime": row["tpep_dropoff_datetime"],
        "passenger_count": float(row["passenger_count"]),
        "trip_distance": float(row["trip_distance"]),
        "RatecodeID": float(row["RatecodeID"]),
        "store_and_fwd_flag": row["store_and_fwd_flag"],
        "PULocationID": int(row["PULocationID"]),
        "DOLocationID": int(row["DOLocationID"]),
        "payment_type": int(row["payment_type"]),
        "fare_amount": float(row["fare_amount"]),
        "extra": float(row["extra"]),
        "mta_tax": float(row["mta_tax"]),
        "tip_amount": float(row["tip_amount"]),
        "tolls_amount": float(row["tolls_amount"]),
        "improvement_surcharge": float(row["improvement_surcharge"]),
        "total_amount": float(row["total_amount"]),
        "congestion_surcharge": float(row["congestion_surcharge"]),
        "Airport_fee": float(row["Airport_fee"]),
        "row_id": row["row_id"]
    }
    
    # API'ye gönder
    response = requests.post(trips_url, headers=headers, json=trip_data)
    print(f"Kayıt {i+1} yanıtı:", response.status_code, response.text)
    time.sleep(1)  # API'yi aşırı yüklememek için

# Kayıtları kontrol et
get_response = requests.get("http://localhost:8000/trips")
print("Kayıtlar:", get_response.json())