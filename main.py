from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")
app.add_middleware(CORSMiddleware,
                   allow_origins=[
                       settings.DOMAIN_NAME,
                       settings.DOMAIN_NAME_2,
                   ],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )




@app.get("/health")
async def health_check():
    return {"status": "ok"}