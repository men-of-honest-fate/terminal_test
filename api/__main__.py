import uvicorn

from api.routes.base import app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
