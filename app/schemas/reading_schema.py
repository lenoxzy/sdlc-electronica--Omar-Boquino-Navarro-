from typing import Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.domain.physics import validate_physics


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

    @model_validator(mode="after")
    def validate_physics_rules(self) -> Self:
        validate_physics(self.value, self.unit)
        return self


class ReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str | None) -> str | None:
        if v is None:
            return v
        valid_units = ["C", "F", "K", "%", "hPa"]
        if v not in valid_units:
            raise ValueError(f"Unidad desconocida. Debe ser una de: {valid_units}")
        return v

    @model_validator(mode="after")
    def validate_physics_rules(self) -> Self:
        # Validación "superficial": solo puede evaluar si AMBOS campos
        # llegan en el mismo patch. El caso de un solo campo lo cubre
        # ReadingService, que sí tiene acceso al valor/unidad ya guardados.
        if self.unit is not None and self.value is not None:
            validate_physics(self.value, self.unit)
        return self


class ReadingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    value: float
    unit: str