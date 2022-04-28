"""Configurations of parameters, initial conditions, and default models for a given simulation."""

from typing import Dict, List
import json
from utils.log import log
from jsonschema import Draft3Validator, ValidationError
from utils.constants import DEFAULT_MODELS, ModelEnum

from core.parameters import Parameters
from core.state import StateTime


class MutationException(Exception):
    pass


class JsonError(Exception):
    pass


class Config:
    """Representation of the parameters and initial conditions of the simulation.
    This module depends on parameters.py, models.py, and state.py.
    The variation in performance of different runs of the simulation depends on the variation of config.
    This class is frozen, so it cannot be changed."""

    _frozen = False

    def __init__(
        self,
        parameters: Dict,
        initial_condition: Dict,
        models: List[ModelEnum] = [ModelEnum.AttitudeModel, ModelEnum.PositionModel],
    ):

        self.param = Parameters(param_dict=parameters)
        self.init_cond = StateTime.from_dict(initial_condition)

        # convert string list to model list
        model_objs = []
        for model in models:
            model_objs.append(model)
        self.models = model_objs  # models is a list of the names of the models that are used in a sim
        self._frozen = True

    def __setattr__(self, __name, __value) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        object.__setattr__(self, __name, __value)

    def __delattr__(self, __name) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        object.__delattr__(self, __name)

    @classmethod
    def make_config(cls, path_str: str):
        """make_config creates a config object from json file in the proposed location.

        It is dependent on state.py, and parameters.py. Changes in these files will affect this method. It will be used by main.py. Changes in this method might affect the functionality of Main.

        To construct a json file, consult schema.json and example.json in the 'configs' folder. All properties are optional, default values will be inserted if a field is not specified. However, if a property is specified its type and format has to be correct.

        Raises: `JsonError` if json file is not well defined.

        """
        with open(path_str, "r") as read_file:
            data = json.load(read_file)
            try:
                Draft3Validator(json.load(open("configs/schema.json", "r"))).validate(
                    data
                )
                # validate(instance=data, schema=json.load(open("configs/schema.json", "r")))
            except ValidationError:
                raise JsonError("Schema validation failed.")

            # Checking if gyro_bias ans gyro_noise are in the correct format if thery are specified. (other type verification is done by schema.json)
            try:  # validate gyro_bias is a list of length 3
                gyro_bias = data.get("parameters").get("gyro_bias")
                if len(gyro_bias) != 3:
                    raise JsonError("gyro_bias is not well defined.")
            except AttributeError:
                pass  # there is no "parameters" in the json
            except TypeError:
                pass  # there is no "gyro_bias" in the json

            try:  # validate gyro_noise is a list of length 3
                gyro_noise = data.get("parameters").get("gyro_noise")
                if len(gyro_noise) != 3:
                    raise JsonError("gyro_noise is not well defined.")
            except AttributeError:
                pass  # there is no "parameters" in the json
            except TypeError:
                pass  # there is no "gyro_noise" in the json

            json_params = data.get("parameters", {})
            if json_params == {}:
                log.warning("parameters are not specified")
            json_init_cond = data.get("initial_condition", {})
            if json_init_cond == {}:
                log.warning("initial conditions are not specified")
            json_models = data.get("models", [])
            if json_models == []:
                log.warning("models are not specified")

            actual_models = []
            for model_str in json_models:
                actual_models.append(ModelEnum(model_str))

        return cls(json_params, json_init_cond, actual_models)
