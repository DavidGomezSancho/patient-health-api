import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

WEIGHT_REGEX = r"^\d+(\.\d+)?\s*(kg|lb|st)$"
PRESS_REGEX = r"^\d{2,3}/\d{2,3}\s*mmHg$"
GLUCOSE_REGEX = r"^\d+(\.\d+)?\s*(mg/dL|mmol/L)$"
GENDER = ["Male", "Female", "Other"]
SEX = ["M", "F", "O"]
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
PHONE_CHECK = r"^\+?\d[\d\s\-]+$"

schema_measure = DataFrameSchema({
    "patient_name": Column(str, nullable=False),
    "email": Column(pa.String, checks=pa.Check.str_matches(EMAIL_REGEX), nullable=False),
    "glucose": Column(str, checks=[
        Check.str_matches(GLUCOSE_REGEX)
    ], nullable=True),
    "blood_pressure": Column(str, checks=[
        Check.str_matches(PRESS_REGEX)
    ], nullable=True),
    "weight": Column(str, checks=[
        Check.str_matches(WEIGHT_REGEX)
    ], nullable=True)
})

schema_patient = pa.DataFrameSchema({
    "name": Column(str, nullable=False),
    "dob": Column(pa.DateTime, nullable=True),
    "gender": Column(str, checks=pa.Check.isin(GENDER),
                     nullable=True),
    "address": Column(str, nullable=True),
    "email": Column(str, nullable=False, checks=pa.Check
                    .str_matches(EMAIL_REGEX)),
    "phone": Column(str, checks=pa.Check.str_matches(PHONE_CHECK), nullable=True),
    "sex": Column(str, checks=pa.Check.isin(SEX), nullable=True),
})