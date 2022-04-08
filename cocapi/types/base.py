from pydantic import BaseModel

from ..utils import toCamel


class DefaultBaseModel(BaseModel):
    """
    Config
    ------
    - mutations are not allowed
    - for every field there is an alias with camelCase
    """

    class Config:
        allow_mutation = False
        alias_generator = toCamel
