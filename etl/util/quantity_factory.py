from .quantity import *

class QuantityFactory:
    _registry: dict[str, tuple[Type[Enum], Type[Quantity]]] = {}

    @classmethod
    def register(cls, unit_enum: Type[Enum], quantity_cls: Type[Quantity]):
        for unit in unit_enum:
            cls._registry[unit.value] = (unit_enum, quantity_cls)

    @classmethod
    def create(cls, value: float, unit_str: str) -> "Quantity":
        if unit_str not in cls._registry:
            raise ValueError(f"Unknown unit: {unit_str}")

        unit_enum, quantity_cls = cls._registry[unit_str]
        unit = unit_enum(unit_str)
        return quantity_cls(value, unit)

QuantityFactory.register(UnitMeasureWeight, WeightQuantity)
QuantityFactory.register(UnitMeasureGlucose, GlucoseQuantity)
QuantityFactory.register(UnitMeasureBloodPress, BloodPressQuantity)


