from fastapi import FastAPI
from DataKeying.Models import Models
from DataKeying.Config.Database import engine
from DataKeying.Controllers import AuthenticationController,ImageDataEntryController,AiImageEntryController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Models.Base.metadata.create_all(engine)

app.include_router(AuthenticationController.router)
app.include_router(ImageDataEntryController.router)
app.include_router(AiImageEntryController.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)