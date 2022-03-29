from enum import Enum
from typing import Union


class StringEnum(str, Enum):
    """Similar to the built-in IntEnum, but with strings!
    See https://docs.python.org/3/library/enum.html#others for inspiration."""

    pass


class ModelEnum(StringEnum):
    AttitudeModel = "att"
    PositionModel = "pos"
    UnittestModel = "unittest"


DEFAULT_MODELS = [ModelEnum.AttitudeModel, ModelEnum.PositionModel]

State_Type = Union[int, float, bool]
