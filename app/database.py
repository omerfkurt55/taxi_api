from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/taxidb")
print(f"Bağlanılacak veritabanı: {DATABASE_URL}")

# Veritabanına bağlantı için yeniden deneme mekanizması
max_retries = 30
for retry in range(max_retries):
    try:
        engine = create_engine(DATABASE_URL)
        # Test bağlantısı
        with engine.connect() as conn:
            pass
        print(f"Veritabanına {retry+1}. denemede başarıyla bağlanıldı.")
        break
    except OperationalError as e:
        if retry < max_retries - 1:
            print(f"Veritabanına bağlanılamadı. Deneme {retry+1}/{max_retries}. 2 saniye sonra tekrar denenecek.")
            time.sleep(2)
        else:
            print(f"Veritabanına {max_retries} denemede bağlanılamadı. Son hata: {e}")
            raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()