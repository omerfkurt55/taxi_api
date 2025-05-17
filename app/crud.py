from sqlalchemy.orm import Session
import hashlib
import json
from . import models, schemas, auth
from datetime import datetime

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_trip(db: Session, trip: schemas.TaxiTripCreate):
    # Row ID oluştur (eğer sağlanmamışsa)
    if not trip.row_id:
        # Row ID için basit bir hash oluştur
        trip_dict = trip.dict()
        trip_dict.pop('row_id', None)
        trip_json = json.dumps(trip_dict, default=str, sort_keys=True)
        trip.row_id = hashlib.md5(trip_json.encode()).hexdigest()
    
    db_trip = models.TaxiTrip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

def get_trips(db: Session, limit: int = 10):
    return db.query(models.TaxiTrip).order_by(models.TaxiTrip.tpep_pickup_datetime.desc()).limit(limit).all()