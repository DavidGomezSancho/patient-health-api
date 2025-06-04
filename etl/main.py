from .load import load
from .extract import extract
from .transform import transform
from .logger_config import get_logger

logger = get_logger(__name__)

def main():

    logger.info("Performing extraction phase.")
    df_patient_reads = extract()
    logger.info("End of extraction phase.")

    logger.info("Initializing transform phase.")
    df_patient_reads_transformed = transform(df_patient_reads)
    logger.info("Finished transform phase.")
    logger.debug(df_patient_reads_transformed)

    logger.info("Initializing load phase.")
    load(df_patient_reads_transformed)
    logger.info("Finished load phase.")

if __name__ == '__main__':
    main()