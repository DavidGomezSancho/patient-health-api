from enum import Enum
from typing import Annotated, List
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Query, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database.model import Patient, MeasureHealth, DerivedMeasureHealth
from database.session import get_db
from .schema import PatientDto, MeasureDto, MeasureUpsertDto, DerivedMeasureHealthDTO

app = FastAPI()
db_dependency = Annotated[Session, Depends(get_db)]

class BiometricType(str, Enum):
    glucose = "glucose"
    weight = "weight"
    pressure = "pressure"

BIOMETRIC_FILTERS = {
    BiometricType.glucose: lambda model: model.glucose.isnot(None),
    BiometricType.weight: lambda model: model.weight.isnot(None),
    BiometricType.pressure: lambda model: and_(model.press_syst.isnot(None), model.press_diast.isnot(None)),
}

@app.get("/patient", response_model=List[PatientDto])
async def read_all(db: db_dependency, page: int = Query(1, ge=1),
                   size: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * size
    patients = db.query(Patient).offset(skip).limit(size).all()
    return patients

@app.get("/patient/{patient_id}/measure", response_model=List[MeasureDto])
async def read_all(db: db_dependency, patient_id: UUID, page: int = Query(1, ge=1),
                   size: int = Query(10, ge=1, le=100),
                   biometric: BiometricType | None = Query(None)):
    patient = get_patient_or_404(db, patient_id)
    skip = (page - 1) * size
    query = db.query(MeasureHealth).filter(MeasureHealth.id_patient == patient.id)
    if filter_func := BIOMETRIC_FILTERS.get(biometric):
        query = query.filter(filter_func(MeasureHealth))
    measures = (query.order_by(MeasureHealth.created_at.desc())
                .offset(skip).limit(size).all())
    return measures

@app.post("/patient/{patient_id}/measure")
async def upsert_measure(db: db_dependency, patient_id: UUID, measure_data: MeasureUpsertDto):
    patient = get_patient_or_404(db, patient_id)

    if measure_data.public_id:
        measure = db.query(MeasureHealth).filter_by(public_id=str(measure_data.public_id)).first()
        if measure:
            update_data = measure_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(measure, field, value)
            db.commit()
            db.refresh(measure)
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                                content={"detail": "Measure updated",
                                         "public_id": measure.public_id})

    new_measure = MeasureHealth(
        **measure_data.model_dump(exclude={"public_id", "created_at"}, exclude_unset=True),
        public_id=str(measure_data.public_id or uuid4()), id_patient=patient.id,
        created_at=measure_data.created_at )

    db.add(new_measure)
    db.commit()
    db.refresh(new_measure)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"detail": "Measure inserted",
                                 "public_id": new_measure.public_id})


@app.delete("/measure/{measure_id}")
async def delete_measure(db: db_dependency, measure_id: UUID):
    measure = db.query(MeasureHealth).filter(MeasureHealth.public_id == str(measure_id)).first()
    if not measure:
        raise HTTPException(status_code=404, detail="Measure not found")

    db.delete(measure)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/patient/{patient_id}/derivedmeasure", response_model=List[DerivedMeasureHealthDTO])
async def read_all(db: db_dependency, patient_id: UUID):
    patient = get_patient_or_404(db, patient_id)
    derived_measures = (db.query(DerivedMeasureHealth)
                        .filter(DerivedMeasureHealth.id_patient == patient.id).all())
    return derived_measures

def get_patient_or_404(db: Session, patient_id: UUID):
    patient = db.query(Patient).filter(Patient.public_id == str(patient_id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient