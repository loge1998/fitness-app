from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import user
from app.routes.tasks import router as task_routes
from app.routes.goals import router as goal_routes
from app.core import auth

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task_routes)
app.include_router(goal_routes)
