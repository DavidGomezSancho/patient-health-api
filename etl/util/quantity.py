from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Tuple, Callable, Generic, TypeVar, Type

CONST_ST_LB = 14
CONST_MMOL_L_MG_DL = 18.02
CONST_G_LB = 2.20462 / 1000
CONST_KG_LB = 2.20462

U = TypeVar("U", bound=Enum)

class Quantity(ABC, Generic[U]):
    _conversions: Dict[Tuple[U, U], Callable[[float], float]] = {}

    def __init__(self, value: float, unit: U):
        if not isinstance(unit, self.unit_enum()):
            raise TypeError(f"Expected unit of type {self.unit_enum().__name__}, got {type(unit).__name__}")
        self.value = value
        self.unit = unit

    @classmethod
    @abstractmethod
    def unit_enum(cls) -> Type[U]:
        """Must return the Enum class of valid units for this quantity"""

    @classmethod
    def add_conversion(cls, origin: U, target: U, func: Callable[[float], float]):
        cls._conversions[(origin, target)] = func

    def to_unit(self, target: U):
        if self.unit == target:
            return
        key = (self.unit, target)
        if key not in self._conversions:
            raise ValueError(f"No conversion from {self.unit} to {target} registered")
        self.value = self._conversions[key](self.value)
        self.unit = target

    @abstractmethod
    def to_us_unit(self):
        """Convert to the corresponding US unit"""

    def __str__(self):
        return f"{self.value} {self.unit.value}"


class UnitMeasureWeight(Enum):
    KG = "kg"
    LB = "lb"
    G = "g"
    ST = "st"

class WeightQuantity(Quantity[UnitMeasureWeight]):
    _conversions: Dict[Tuple[UnitMeasureWeight, UnitMeasureWeight], Callable[[float], float]] = {}

    @classmethod
    def unit_enum(cls) -> Type[UnitMeasureWeight]:
        return UnitMeasureWeight

    def to_us_unit(self):
        return self.to_unit(UnitMeasureWeight.LB)


class UnitMeasureGlucose(Enum):
    MMOL_L = "mmol/L"
    MG_DL = "mg/dL"

class GlucoseQuantity(Quantity[UnitMeasureGlucose]):
    _conversions: Dict[Tuple[UnitMeasureGlucose, UnitMeasureGlucose], Callable[[float], float]] = {}

    @classmethod
    def unit_enum(cls) -> Type[UnitMeasureGlucose]:
        return UnitMeasureGlucose

    def to_us_unit(self):
        return self.to_unit(UnitMeasureGlucose.MG_DL)


class UnitMeasureBloodPress(Enum):
    MMHG = "mmHg"

class BloodPressQuantity(Quantity[UnitMeasureBloodPress]):
    _conversions: Dict[Tuple[UnitMeasureBloodPress, UnitMeasureBloodPress], Callable[[float], float]] = {}

    @classmethod
    def unit_enum(cls) -> Type[UnitMeasureBloodPress]:
        return UnitMeasureBloodPress

    def to_us_unit(self):
        return self.to_unit(UnitMeasureBloodPress.MMHG)

# Register conversions
WeightQuantity.add_conversion(UnitMeasureWeight.KG, UnitMeasureWeight.LB,
                              lambda v: v * CONST_KG_LB)
WeightQuantity.add_conversion(UnitMeasureWeight.G, UnitMeasureWeight.LB,
                              lambda v: v * CONST_G_LB)
WeightQuantity.add_conversion(UnitMeasureWeight.ST, UnitMeasureWeight.LB,
                              lambda v: v * CONST_ST_LB)
GlucoseQuantity.add_conversion(UnitMeasureGlucose.MMOL_L, UnitMeasureGlucose.MG_DL,
                               lambda v: v * CONST_MMOL_L_MG_DL)
