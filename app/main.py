from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
import os
import time
import psycopg2
from sqlalchemy.exc import OperationalError

from . import crud, models, schemas, auth
from .database import engine, get_db

# PostgreSQL bağlantısını bekleyen fonksiyon
def wait_for_db(max_retries=10, retry_interval=3):
    retries = 0
    while retries < max_retries:
        try:
            # Bağlantıyı test et
            conn = psycopg2.connect(
                host="postgres",
                port=5432,
                user="postgres",
                password="postgres",
                database="taxidb"
            )
            conn.close()
            print("PostgreSQL bağlantısı başarılı!")
            return True
        except psycopg2.OperationalError as e:
            retries += 1
            print(f"PostgreSQL'e bağlanılamıyor. Deneme {retries}/{max_retries}. Hata: {e}")
            if retries >= max_retries:
                return False
            time.sleep(retry_interval)

# Veritabanının hazır olmasını bekle
wait_for_db(max_retries=30, retry_interval=2)

try:
    # Veritabanı tablolarını oluştur
    models.Base.metadata.create_all(bind=engine)
    print("Veritabanı tabloları başarıyla oluşturuldu.")
except Exception as e:
    print(f"Veritabanı tabloları oluşturulurken hata oluştu: {e}")

app = FastAPI(title="Taxi Trip API")

@app.get("/")
def read_root():
    return {"message": "Taxi Trip API is running"}


@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Kullanıcı adı zaten kullanımda"
        )
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/trips", response_model=schemas.TaxiTripResponse)
def create_taxi_trip(
    trip: schemas.TaxiTripCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_trip(db=db, trip=trip)

@app.get("/trips", response_model=List[schemas.TaxiTripResponse])
def read_trips(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, le=10)
):
    trips = crud.get_trips(db, limit=limit)
    return trips