from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# To handle ObjectId serialization
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema):
        return {
            "type": "string",
            "format": "objectid",
        }

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    email: str
    password: str

    class Config:
      validate_by_name = True
      arbitrary_types_allowed = True
      json_encoders = {
          ObjectId: str
      }
      from_attributes = True
