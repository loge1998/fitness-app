from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import userRoutes
from app.routes.tasks import router as task_routes
# from app.core import auth

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router)
app.include_router(userRoutes.router)
app.include_router(task_routes)
