# -*- coding: utf-8 -*-
"""Module to define input data schemas, to be validated after read."""

import pandera as pa
from pandera.typing import Series


class SampleSchema(pa.DataFrameModel):
    """Schema for sample data."""

    product: Series[str] = pa.Field(unique=True, nullable=False, coerce=True)
    color: Series[str] = pa.Field(unique=True, nullable=True)
    price: Series[float] = pa.Field(ge=0, nullable=False, coerce=True)
