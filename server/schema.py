from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

class PatientDto(BaseModel):
    name: str
    dob: datetime
    gender: str
    sex: str
    address: str
    email: str
    phone: str
    public_id: str

    class Config:
        orm_mode = True

class MeasureDto(BaseModel):
    weight: float | None
    glucose: float | None
    press_syst: int | None
    press_diast: int | None
    created_at: datetime
    public_id: str

    class Config:
        orm_mode = True

class MeasureUpsertDto(BaseModel):
    public_id: Optional[UUID] = None
    weight: Optional[float] = None
    glucose: Optional[float] = None
    press_syst: Optional[int] = None
    press_diast: Optional[int] = None
    created_at: Optional[datetime] = None

class DerivedMeasureHealthDTO(BaseModel):
    max_weight: Optional[float] = None
    min_weight: Optional[float] = None
    av_weight: Optional[float] = None
    max_glucose: Optional[float] = None
    min_glucose: Optional[float] = None
    av_glucose: Optional[float] = None
    max_press_syst: Optional[int] = None
    min_press_syst: Optional[int] = None
    av_press_syst: Optional[float] = None
    max_press_diast: Optional[int] = None
    min_press_diast: Optional[int] = None
    av_press_diast: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True