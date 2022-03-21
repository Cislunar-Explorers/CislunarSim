from typing import List, Dict, Type
from core.models.model import Model
from core.config import Config
from utils.constants import ModelEnum


class AttitudeDynamics(Model):
    ...


class PositionDynamics(Model):
    ...



# Dict containing all the models that are implemented
MODEL_DICT: Dict[ModelEnum, Type[Model]] = {
    ModelEnum.AttitudeModel: AttitudeDynamics,
    ModelEnum.PositionModel: PositionDynamics,
}


def build_models(config: Config) -> List[Model]:
    models = []

    for model_name in config.models:
        model = MODEL_DICT[model_name](config.param)
        models.append(model)

    return models
