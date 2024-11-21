import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date, datetime


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    dob: date
    address: str
    gender: str
    email: EmailStr
    phone_number: str
    added_on = datetime.now()

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must be a 10-digit number")
        return value


class UserUpdate(BaseModel):
    firstname: Optional[str] = Field(None, max_length=50)
    lastname: Optional[str] = Field(None, max_length=50)
    dob: Optional[date]
    address: Optional[str] = Field(None, max_length=200)
    gender: Optional[str] = Field(None, max_length=10)
    email: Optional[EmailStr]
    phone_number: Optional[str]
    updated_on = datetime.now()
