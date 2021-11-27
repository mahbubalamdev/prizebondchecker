from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum


from api.v1.api import router as api_router

app = FastAPI(title="Serverless Lambda FastAPI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def main():
    return {"message": "Hello World"}


def handler(event, context):
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response
