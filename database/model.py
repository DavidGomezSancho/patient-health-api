import uuid

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
    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False,
                       index=True)
    __table_args__ = (Index('ix_patient_name_email', 'name', 'email', unique=True),)

    measures = relationship("MeasureHealth", back_populates="patient")
    derivedmeasures = relationship("DerivedMeasureHealth", back_populates="patient")

class MeasureHealth(Base):
    __tablename__ = 'measure_health'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey('patient.id'), nullable=False, index=True)
    weight = Column(Float)
    glucose = Column(Float)
    press_syst = Column(Integer)
    press_diast = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False,
                       index=True)

    patient = relationship("Patient", back_populates="measures")

class DerivedMeasureHealth(Base):
    __tablename__ = 'derived_measure_health'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey('patient.id'), nullable=False, unique=True, index=True)
    max_weight = Column(Float)
    min_weight = Column(Float)
    av_weight = Column(Float)
    max_glucose = Column(Float)
    min_glucose = Column(Float)
    av_glucose = Column(Float)
    max_press_syst = Column(Integer)
    min_press_syst = Column(Integer)
    av_press_syst = Column(Float)
    max_press_diast = Column(Integer)
    min_press_diast = Column(Integer)
    av_press_diast = Column(Float)
    created_at = Column(DateTime, default=func.now())

    patient = relationship("Patient", back_populates="derivedmeasures")