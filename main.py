#OM VIGHNHARTAYE NAMO NAMAH :
from fastapi import FastAPI 
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.roleCrud.role import router as roleRouter
from app.api.parameterCRUD.parameter import router as parameterRouter
from app.api.permisisonCRUD.permission import router as permsisonRouter
from app.api.UserCRUD.user import router as userRouter
from app.api.sensor_data.sensorData import router as sensordataRouter
from app.api.kafka_consumer.websocket import router as wsRouter

def include_routers(app):
    app.include_router(wsRouter)
    app.include_router(sensordataRouter)
    app.include_router(roleRouter)
    app.include_router(parameterRouter)
    app.include_router(permsisonRouter)
    app.include_router(userRouter)
    return



def start_application():
    app = FastAPI(docs_url="/api/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"], 
    )
    app.mount("/web", StaticFiles(directory="static", html=True), name="static")

    include_routers(app)

    return app

app = start_application()