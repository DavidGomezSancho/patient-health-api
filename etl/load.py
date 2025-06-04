import pandas as pd
from sqlalchemy import tuple_

from database.decorator import use_db
from database.model import Patient, MeasureHealth


@use_db
def load(df: pd.DataFrame, db):
    unique_keys = set((row.email, row.name) for row in df[['email', 'name']]
                      .itertuples(index=False))
    existing_patients = db.query(Patient).filter(
        tuple_(Patient.email, Patient.name).in_(unique_keys)).all()
    patient_index = {(p.email, p.name): p for p in existing_patients}

    for row in (df[['name', 'dob', 'gender', 'sex', 'address', 'email', 'phone', 'glucose_normalized',
                   'weight_normalized', 'blood_pressure_syst', 'blood_pressure_diast']]
            .itertuples(index=False)):
        key = (row.email, row.name)
        patient = patient_index.get(key)

        if not patient:
            patient = Patient(name=row.name, dob=row.dob, gender=row.gender,sex=row.sex,
                              address=row.address, email=row.email, phone=row.phone)
            db.add(patient)
            db.flush()
            patient_index[key] = patient
        db.add(MeasureHealth(weight=row.weight_normalized.value, glucose=row.glucose_normalized.value,
                             press_syst=row.blood_pressure_syst.value,
                             press_diast=row.blood_pressure_diast.value, patient=patient))
    db.commit()
