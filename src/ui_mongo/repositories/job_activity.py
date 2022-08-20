from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class JobActivityType(Enum):
    employer_contact = "employer_contact"
    worksource = "worksource"
    other = "other"


class JobActivity(BaseModel):
    activity_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: JobActivityType = JobActivityType.employer_contact
    desc: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
                        "example": {
                            "type": "employer_contact",
                        }
                    }


class EmployerContactActivity(JobActivity):
    type = JobActivityType.employer_contact
    desc: str
    link: Optional[str]


class WorkSourceActivity(JobActivity):
    type = JobActivityType.worksource
    desc: str
    file: Optional[str]


class OtherActivity(JobActivity):
    type = JobActivityType.other
    desc: str
    file: Optional[str]
    link: Optional[str]
