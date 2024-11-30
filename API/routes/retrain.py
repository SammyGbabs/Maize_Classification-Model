from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
import os
import zipfile
import uuid
import shutil
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from fastapi.responses import FileResponse

# FastAPI Router
router = APIRouter()

# Base directory for uploads and preprocessing
BASE_DIR = './data'
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
PREPROCESSED_DIR = os.path.join(BASE_DIR, 'preprocessed_images')

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

# Function to create unique directories for each upload
def create_unique_directory(base_dir: str) -> str:
    """Creates a unique directory for each upload."""
    unique_id = str(uuid.uuid4())  # Generate a unique identifier
    unique_dir = os.path.join(base_dir, unique_id)
    os.makedirs(unique_dir, exist_ok=True)
    return unique_dir

# Function to unzip the uploaded ZIP file
def unzip_file(zip_file_path: str, extract_to: str):
    """Unzips the uploaded file into the given directory."""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Preprocess the dataset and organize it into class subdirectories
def organize_dataset(unzipped_dir: str, output_dir: str):
    """Organize images into class subdirectories for retraining."""
    for root, dirs, files in os.walk(unzipped_dir):
        for file_name in files:
            if file_name.endswith(('.png', '.jpg', '.jpeg')):
                class_name = os.path.basename(root)  # Folder name is the class name
                class_dir = os.path.join(output_dir, class_name)
                if not os.path.exists(class_dir):
                    os.makedirs(class_dir)
                # Move the file to the appropriate class folder
                source_path = os.path.join(root, file_name)
                dest_path = os.path.join(class_dir, file_name)
                shutil.move(source_path, dest_path)

# Function to retrain the model
def retrain_model(model_path: str, dataset_dir: str):
    """Retrains the existing model with new data."""
    # Load the existing model
    model = load_model(model_path)

    # Recreate the optimizer
    optimizer = tf.keras.optimizers.Adam()

    # Recompile the model with the new optimizer
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Set up the data generator
    datagen = ImageDataGenerator(rescale=1.0/255.0, validation_split=0.2)

    # Train and validation generators
    train_gen = datagen.flow_from_directory(
        dataset_dir,
        target_size=(256, 256),
        batch_size=32,
        class_mode='sparse',  # Use sparse labels to match original model
        subset='training'
    )
    val_gen = datagen.flow_from_directory(
        dataset_dir,
        target_size=(256, 256),
        batch_size=32,
        class_mode='sparse',  # Use sparse labels to match original model
        subset='validation'
    )

    # Retrain the model
    model.fit(
        train_gen,
        epochs=1,  
        validation_data=val_gen,
        verbose=1
    )

    # Evaluate the model on the validation set
    evaluation = model.evaluate(val_gen, verbose=1)

    # Save the retrained model with a fixed name
    retrained_model_path = os.path.join(BASE_DIR, "models", "model_densenet_retrained.h5")
    model.save(retrained_model_path)

    # Return evaluation metrics along with the model path
    return retrained_model_path, evaluation

# In routes/retrain.py
@router.get("")
async def test_retrain_endpoint():
    return {"message": "Retrain endpoint is working"}

@router.post("/upload")
async def upload_and_retrain(file: UploadFile = File(...)):
    """Uploads a ZIP file, preprocesses images, and retrains the model."""
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are supported.")
    
    # Step 1: Create a unique directory for this upload
    unique_dir = create_unique_directory(UPLOAD_DIR)
    
    # Step 2: Save the uploaded file in the unique directory
    zip_path = os.path.join(unique_dir, file.filename)
    with open(zip_path, "wb") as f:
        f.write(await file.read())
    
    # Step 3: Unzip the file
    unzipped_dir = os.path.join(unique_dir, "unzipped")
    os.makedirs(unzipped_dir, exist_ok=True)
    unzip_file(zip_path, unzipped_dir)

    # Step 4: Organize the dataset into class subdirectories
    organize_dataset(unzipped_dir, PREPROCESSED_DIR)

    # Step 5: Retrain the model
    model_path = "../models/model_densenet.h5"  # Path to the existing model
    try:
        retrained_model_path, evaluation_metrics = retrain_model(model_path, PREPROCESSED_DIR)
        return {
            "message": "Model retrained successfully.",
            "model_path": retrained_model_path,
            "evaluation": {
                "loss": evaluation_metrics[0],
                "accuracy": evaluation_metrics[1]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during model retraining: {e}")


@router.get("/download-model")
async def download_model():
    """Endpoint to download the retrained model."""
    retrained_model_path = "./models/model_densenet_retrained.h5"
    if os.path.exists(retrained_model_path):
        return FileResponse(
            retrained_model_path,
            media_type='application/octet-stream',
            filename="model_densenet_retrained.h5"
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="Retrained model not found. Please retrain the model first."
        )
