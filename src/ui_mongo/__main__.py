import uvicorn
from ui_mongo import config

uvicorn.run("ui_mongo.api:app",
            host=config.settings.host_ip,
            port=config.settings.host_port,
            reload=True)
