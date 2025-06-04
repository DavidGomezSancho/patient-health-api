from sqlalchemy import func
from database.decorator import use_db
from database.model import Patient, MeasureHealth, DerivedMeasureHealth

BATCH_SIZE = 100

@use_db
def calculate_measures(db):
    patient_ids = db.query(Patient.id.distinct()).all()
    patient_ids = [pat_id[0] for pat_id in patient_ids]
    for i in range(0, len(patient_ids), BATCH_SIZE):
        batch_ids = patient_ids[i:i + BATCH_SIZE]

        db.query(DerivedMeasureHealth).filter(
            DerivedMeasureHealth.id_patient.in_(batch_ids)
        ).delete(synchronize_session=False)

        results = (
            db.query(
                MeasureHealth.id_patient,
                func.max(MeasureHealth.weight).label("max_weight"),
                func.min(MeasureHealth.weight).label("min_weight"),
                func.avg(MeasureHealth.weight).label("av_weight"),
                func.max(MeasureHealth.glucose).label("max_glucose"),
                func.min(MeasureHealth.glucose).label("min_glucose"),
                func.avg(MeasureHealth.glucose).label("av_glucose"),
                func.max(MeasureHealth.press_syst).label("max_press_syst"),
                func.min(MeasureHealth.press_syst).label("min_press_syst"),
                func.avg(MeasureHealth.press_syst).label("av_press_syst"),
                func.max(MeasureHealth.press_diast).label("max_press_diast"),
                func.min(MeasureHealth.press_diast).label("min_press_diast"),
                func.avg(MeasureHealth.press_diast).label("av_press_diast"))
            .filter(MeasureHealth.id_patient.in_(batch_ids))
            .group_by(MeasureHealth.id_patient)
            .all())

        new_records  = [
            DerivedMeasureHealth(
                id_patient=row.id_patient,
                max_weight=row.max_weight,
                min_weight=row.min_weight,
                av_weight=row.av_weight,
                max_glucose=row.max_glucose,
                min_glucose=row.min_glucose,
                av_glucose=row.av_glucose,
                max_press_syst=row.max_press_syst,
                min_press_syst=row.min_press_syst,
                av_press_syst=row.av_press_syst,
                max_press_diast=row.max_press_diast,
                min_press_diast=row.min_press_diast,
                av_press_diast=row.av_press_diast)
            for row in results]
        db.bulk_save_objects(new_records)
        db.commit()