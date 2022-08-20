#  (c) Copyright  2022 Michael Penhallegon <mike@hematite.tech>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import List

from fastapi import APIRouter, Body
import logging

from fastapi.encoders import jsonable_encoder
from starlette import status

from starlette.responses import JSONResponse

from ui_mongo.globals import db
from ui_mongo.metrics import EntryTransactionType, transaction_metric
from ui_mongo.repositories.job_activity import JobActivity

log = logging.getLogger("__name__")
router = APIRouter(tags=["docs"])


@transaction_metric(EntryTransactionType.get)
@router.get("/job_activity/", response_model=List[JobActivity])
async def get_activities():
    job_activities = await db["job_activity"].find().to_list(1000)
    return job_activities


@transaction_metric(EntryTransactionType.get)
@router.get("/job_activity/{activity_id}/", response_model=JobActivity)
async def get_activity(activity_id: str):
    activity = await db["job_activity"].find_one({"_id": activity_id})
    return JSONResponse(activity)


@transaction_metric(EntryTransactionType.post)
@router.post("/job_activity/", response_model=JobActivity)
async def new_activity(job_activity: JobActivity = Body(...)) -> JSONResponse:
    job_activity = jsonable_encoder(job_activity)
    new_job_activity = await db["job_activity"].insert_one(job_activity)
    created_job_activity = await db["job_activity"].find_one(
        {"_id": new_job_activity.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_job_activity
        )


@transaction_metric(EntryTransactionType.put)
@router.put("/job_activity/{activity_id}/")
async def update_activity(activity_id):
    update_job_activity = await db["job_activity"].find_one(activity_id)
    update_job_activity._id
    return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)


@transaction_metric(EntryTransactionType.delete)
@router.delete("/job_activity/{activity_id}/")
async def delete_activity(activity_id):
    delete_result = await db["job_activity"].delete_one({"_id": activity_id})
    if delete_result.deleted_count == 1:
        return

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
