from fastapi import FastAPI
from API.routes.prediction import router as prediction_router
from API.routes.retrain import router as retrain_router

app = FastAPI(
    title="Maize Leaf Disease Detection API",
    description="An API to predict maize leaf diseases, visualize data, upload datasets, and retrain models.",
    version="1.0.0",
)

# Register routes
app.include_router(prediction_router, prefix="/predict", tags=["Prediction"])
app.include_router(retrain_router, prefix="/retrain", tags=["Retraining"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Maize Leaf Disease Detection API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)