import logging

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from ui_mongo.routers import health, job_activity
from starlette_prometheus import metrics, PrometheusMiddleware

# constants & variables
log = logging.getLogger(__name__)
app = FastAPI()


# Routers
app.include_router(health.router)
app.include_router(job_activity.router)

app.add_middleware(GZipMiddleware)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)


# Startup & Shutdown
@app.on_event("startup")
def setup_app():
    log.info("Application starting...")


@app.on_event("shutdown")
def breakdown_app():
    log.info("Breaking down application...")
