from pydantic import BaseModel, Field
from typing_extensions import Annotated


class Bank1Model(BaseModel):
    timestamp: str
    type: str
    amount: int
    to: int
    frm: Annotated[int, Field(alias="from")]

    class Config:
        allow_population_by_field_name = True


class Bank2Model(BaseModel):
    date: str
    transaction: str
    amounts: int
    to: int
    frm: Annotated[int, Field(alias="from")]

    class Config:
        allow_population_by_field_name = True


class Bank3Model(BaseModel):
    date_readable: str
    type: str
    euro: int
    cents: int
    to: int
    frm: Annotated[int, Field(alias="from")]

    class Config:
        allow_population_by_field_name = True


