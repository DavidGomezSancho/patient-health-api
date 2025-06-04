from pandas import DataFrame

from .util.quantity_factory import QuantityFactory
from .util.quantity import *
from .logger_config import get_logger

logger = get_logger(__name__)

def transform(df: DataFrame) -> DataFrame:
    # Due to I assume we are processing data from the USA I set their units of
    # measurement
    df["glucose_normalized"] = df["glucose"].apply(parse_to_quantity)
    df["weight_normalized"] = df["weight"].apply(parse_to_quantity)

    df[['blood_pressure_syst', 'blood_pressure_diast']] = (
        df['blood_pressure'].str.extract(r'(\d+)/(\d+)').astype(str)
        .apply(lambda col: col + ' mmHg'))
    df['blood_pressure_syst'] = df['blood_pressure_syst'].apply(parse_to_quantity)
    df['blood_pressure_diast'] = df['blood_pressure_diast'].apply(parse_to_quantity)

    logger.debug(df)
    return df

def parse_to_quantity(string):
    value_str, unit_str = string.split(" ")
    quantity = QuantityFactory.create(float(value_str), unit_str)
    quantity.to_us_unit()
    return quantity