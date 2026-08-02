from typing import Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class ReadingCreate(BaseModel):
    value: float
    unit: str

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str) -> str:
        valid_units = ["C", "F", "K", "%", "hPa"]
        if v not in valid_units:
            raise ValueError(f"Unidad desconocida. Debe ser una de: {valid_units}")
        return v

    # ✅ FIX: usar @model_validator(mode='after') para que AMBOS campos
    # ya estén disponibles y validados cuando se comprueba la física
    @model_validator(mode="after")
    def validate_physics(self) -> Self:
        unit = self.unit
        v = self.value

        if unit == "C" and v < -273.15:
            raise ValueError(
                "La temperatura no puede ser menor al cero absoluto (-273.15 °C)"
            )
        if unit == "F" and v < -459.67:
            raise ValueError(
                "La temperatura no puede ser menor al cero absoluto (-459.67 °F)"
            )
        if unit == "K" and v < 0:
            raise ValueError("La temperatura Kelvin no puede ser negativa")
        if unit == "%" and (v < 0 or v > 100):
            raise ValueError("La humedad debe estar entre 0% y 100%")
        if unit == "hPa" and v < 0:
            raise ValueError("La presión no puede ser negativa")

        return self


class ReadingOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )  # ✅ FIX: Config moderna Pydantic v2

    id: int
    value: float
    unit: str
