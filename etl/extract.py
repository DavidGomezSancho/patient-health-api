import pandas as pd
from datetime import datetime
from pandas import DataFrame
from pandera.errors import SchemaErrors
from pandera.pandas import DataFrameSchema
from .schema import schema_patient, schema_measure
from .logger_config import get_logger

logger = get_logger(__name__)

pd.set_option('display.max_columns', None)

def validate_dataframe(df: pd.DataFrame, schema: DataFrameSchema, name: str,
                       invalid_output_basename: str = "invalid_rows"):
    try:
        df_valid = schema.validate(df, lazy=True)
        df_invalid = pd.DataFrame()
    except SchemaErrors as err:
        failed_indexes = err.failure_cases["index"].unique()
        df_valid = err.data[~err.data.index.isin(failed_indexes)]
        df_invalid = err.data[err.data.index.isin(failed_indexes)].copy()
        error_msgs = (err.failure_cases.groupby("index")["failure_case"]
                      .apply(lambda x: "; ".join(set(x))))
        df_invalid["validation_error"] = df_invalid.index.map(error_msgs)

        # invalid_output_basename = f"./log/{invalid_output_basename}_{name}"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"./log/{timestamp}_{invalid_output_basename}_{name}.csv"

        df_invalid.to_csv(filename, index=False)
        logger.error(f"Se exportaron {len(df_invalid)} filas inválidas a '{filename}'.")
    logger.info(f"Se han validado correctamente {len(df_valid)} filas.")

    return df_valid, df_invalid

def extract() -> DataFrame:
    dev_reads_input_cols = list(schema_measure.columns.keys())
    df_device_reads = pd.read_csv("./source/device_reads.csv",
                                  sep=",", usecols=dev_reads_input_cols)
    df_dev_reads_valid, df_dev_reads_invalid = validate_dataframe(df_device_reads,schema_measure,
                                                                  name="device_reads")
    logger.debug("\n Valid measurement input data:")
    logger.debug(f"\n {df_dev_reads_valid}")

    logger.debug("\n Invalid measurement input data:")
    logger.debug(f"\n {df_dev_reads_invalid}")

    df_patients = pd.read_json("./source/patients.json")
    df_patients["dob"] = pd.to_datetime(df_patients["dob"], errors="coerce")
    df_patients_valid, df_patients_invalid = validate_dataframe(df_patients, schema_patient,
                                                                name="patients")
    logger.debug("\n Valid patient input data:")
    logger.debug(f"\n {df_patients_valid}")

    logger.debug("\n Invalid patient data with error:")
    logger.debug(f"\n {df_patients_invalid}")

    merged = pd.merge(df_patients_valid, df_dev_reads_valid, left_on=['name', 'email'],
                      right_on=['patient_name', 'email'], how='inner',
                      suffixes=('_patient', '_dev_read'))
    merged = merged.drop(columns="patient_name")
    logger.debug(f"\n {merged}")
    return merged

if __name__ == '__main__':
    extract()