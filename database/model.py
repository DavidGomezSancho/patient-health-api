from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy import Column, Integer, String, DateTime, CHAR, Index, ForeignKey, Float, func

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    dob = Column(DateTime)
    gender = Column(String)
    sex = Column(CHAR)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    __table_args__ = (Index('ix_patient_name_email', 'name', 'email', unique=True),)

    measures = relationship("MeasureHealth", back_populates="patient")

class MeasureHealth(Base):
    __tablename__ = 'measure_health'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey('patient.id'), nullable=False)
    weight = Column(Float)
    glucose = Column(Float)
    press_syst = Column(Integer)
    press_diast = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    patient = relationship("Patient", back_populates="measures")


