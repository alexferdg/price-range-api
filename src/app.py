# Entry point of the application
from fastapi import FastAPI
from routes import router as mobile_price_range
import uvicorn


# Application
app = FastAPI()
app.include_router(mobile_price_range, tags=["mobile"], prefix = "/mobile")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

# http://localhost:8000/docs to see the Swagger UI