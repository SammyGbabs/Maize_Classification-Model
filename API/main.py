from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.prediction import router as prediction_router
from routes.retrain import router as retrain_router
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="Maize Leaf Disease Detection API",
    description="An API to predict maize leaf diseases, visualize data, upload datasets, and retrain models.",
    version="1.0.0",
)

# Add CORS middleware with local frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Add your local frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(prediction_router, prefix="/predict", tags=["Prediction"])
app.include_router(retrain_router, prefix="/retrain", tags=["Retraining"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Maize Leaf Disease Detection API"}

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to port 8000 if not set
    uvicorn.run(app, host="0.0.0.0", port=port)
