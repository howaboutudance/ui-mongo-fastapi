from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, Body, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ui_mongo.routers import health
from ui_mongo import config
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from bson import ObjectId
import motor.motor_asyncio
# constants & variables
app = FastAPI()

# Routers
app.include_router(health.router)
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(config.settings.mongodb_url)
db = mongo_client.college


# Startup & Shutdown


# Models
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
    desc: str
    file: Optional[str]

class OtherActivity(JobActivity):
    type = JobActivityType.other
    desc: str
    file: Optional[str]
    link: Optional[str]



# Handlers
@app.get("/job_activity/", response_model=List[JobActivity])
async def get_activities():
    job_activities = await db["job_activity"].find().to_list(1000)
    return job_activities



@app.get("/job_activity/{activity_id}/", response_model=JobActivity)
async def get_activity(activity_id: str):
    activity = await db["activity"].find_one({"_id": activity_id})
    return activity

@app.post("/job_activity/", response_model=JobActivity)
async def new_activity(job_activity: JobActivity = Body(...)) -> JSONResponse:
    job_activity = jsonable_encoder(job_activity)
    new_job_activity = await db["job_activity"].insert_one(job_activity)
    created_job_activity = await db["job_activity"].find_one(
        {"_id": new_job_activity.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_job_activity
        )

@app.put("/job_activity/{activity_id}")
def update_activity(activity_id):
    pass


@app.delete("/job_activity/{activity_id}")
def delete_activity(activity_id):
    pass