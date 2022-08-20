from fastapi import APIRouter
import logging


log = logging.getLogger("__name__")
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/status")
def status():
    return "OK"
