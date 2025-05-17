from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TaxiTripBase(BaseModel):
    VendorID: int
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: float
    trip_distance: float
    RatecodeID: float
    store_and_fwd_flag: str
    PULocationID: int
    DOLocationID: int
    payment_type: int
    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float
    improvement_surcharge: float
    total_amount: float
    congestion_surcharge: float
    Airport_fee: float

class TaxiTripCreate(TaxiTripBase):
    row_id: Optional[str] = None

class TaxiTripResponse(TaxiTripBase):
    row_id: str

    class Config:
        orm_mode = True