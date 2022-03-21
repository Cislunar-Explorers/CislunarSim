from typing import List, Dict
from core.models.model import Model

MODEL_LIST: Dict[str, Model] = {}

class ModelEnum(StringEnum):
    

def build_models(models_to_build: List[str]) -> List[Model]:
    for model in models_to_build:


class AttitudeDynamics(Model):
    ...

class PositionDynamics(Model):
    ...