from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
import os
import shutil
import zipfile
import logging
from typing import Dict, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Router initialization
router = APIRouter()

class ModelManager:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.models_dir = self.base_path / "models"
        self.data_dir = self.base_path / "data"
        self.uploads_dir = self.data_dir / "uploads"
        self.preprocessed_dir = self.data_dir / "preprocessed"
        
        # Create necessary directories
        for directory in [self.models_dir, self.uploads_dir, self.preprocessed_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_model_path(self, model_name: str) -> Path:
        """Get the path for a model file."""
        return self.models_dir / f"{model_name}.h5"
    
    def validate_model_exists(self, model_name: str) -> bool:
        """Check if a model exists."""
        model_path = self.get_model_path(model_name)
        return model_path.exists()

class DataProcessor:
    def __init__(self, manager: ModelManager):
        self.manager = manager
    
    async def save_upload(self, file: UploadFile) -> Path:
        """Save uploaded file and return its path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_path = self.manager.uploads_dir / f"upload_{timestamp}.zip"
        
        try:
            content = await file.read()
            upload_path.write_bytes(content)
            return upload_path
        except Exception as e:
            logger.error(f"Error saving upload: {e}")
            raise HTTPException(status_code=500, detail="Failed to save uploaded file")
    
    def validate_zip(self, zip_path: Path) -> Tuple[bool, str]:
        """Validate ZIP file contents."""
        try:
            image_count = 0
            class_dirs = set()
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_path in zip_ref.namelist():
                    if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_count += 1
                        class_dir = Path(file_path).parent
                        if class_dir != Path(''):
                            class_dirs.add(str(class_dir))
            
            if image_count == 0:
                return False, "No valid images found in ZIP file"
            if len(class_dirs) < 2:
                return False, "ZIP must contain images in at least 2 class directories"
                
            return True, f"Found {image_count} images in {len(class_dirs)} classes"
        except Exception as e:
            return False, f"Invalid ZIP file: {str(e)}"
    
    def process_dataset(self, zip_path: Path) -> Path:
        """Process uploaded dataset."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_dir = self.manager.preprocessed_dir / f"dataset_{timestamp}"
        
        try:
            # Extract ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_dir)
            
            # Validate extracted content
            image_count = 0
            for root, _, files in os.walk(dataset_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_count += 1
            
            if image_count == 0:
                raise ValueError("No valid images found after extraction")
                
            return dataset_dir
        except Exception as e:
            if dataset_dir.exists():
                shutil.rmtree(dataset_dir)
            raise HTTPException(status_code=500, detail=f"Dataset processing failed: {str(e)}")

class ModelTrainer:
    def __init__(self, manager: ModelManager):
        self.manager = manager
    
    def setup_data_generators(self, dataset_path: Path) -> Tuple[ImageDataGenerator, ImageDataGenerator]:
        """Setup data generators for training and validation."""
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            validation_split=0.2
        )
        
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2
        )
        
        return train_datagen, val_datagen
    
    def train_model(self, model_name: str, dataset_path: Path) -> Dict:
        try:
            # Load model
            model_path = self.manager.get_model_path(model_name)
            model = load_model(model_path)
            
            # Get number of classes from the dataset directory
            num_classes = len([d for d in dataset_path.iterdir() if d.is_dir()])
            
            # Check output layer shape
            if model.output_shape[-1] != num_classes:
                logger.info(f"Adjusting model output from {model.output_shape[-1]} to {num_classes} classes")
                # Keep all layers except the last one
                x = model.layers[-2].output
                new_output = Dense(num_classes, activation='softmax', name='new_output')(x)
                model = Model(inputs=model.input, outputs=new_output)
            
            # Recompile the model
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # Setup data generators
            train_datagen, val_datagen = self.setup_data_generators(dataset_path)
            
            # Create generators
            train_generator = train_datagen.flow_from_directory(
                dataset_path,
                target_size=(256, 256),
                batch_size=32,
                class_mode='categorical',
                subset='training'
            )
            
            validation_generator = val_datagen.flow_from_directory(
                dataset_path,
                target_size=(256, 256),
                batch_size=32,
                class_mode='categorical',
                subset='validation'
            )
            
            logger.info(f"Retraining model with {num_classes} classes")
            logger.info(f"Found {train_generator.samples} training samples")
            logger.info(f"Found {validation_generator.samples} validation samples")
            
            # Train
            history = model.fit(
                train_generator,
                validation_data=validation_generator,
                epochs=1,
                callbacks=[ 
                    tf.keras.callbacks.EarlyStopping(
                        monitor='val_loss',
                        patience=2,
                        restore_best_weights=True
                    )
                ]
            )
            
            # Log training metrics
            logger.info(f"Training completed. Final accuracy: {history.history['accuracy'][-1]:.4f}")
            logger.info(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
            logger.info(f"Final loss: {history.history['loss'][-1]:.4f}")
            logger.info(f"Final validation loss: {history.history['val_loss'][-1]:.4f}")
            
            # Save retrained model
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_model_path = self.manager.models_dir / f"{model_name}_retrained_{timestamp}.h5"
            model.save(new_model_path)
            
            return {
                "message": "Model retrained successfully",
                "model_path": str(new_model_path),
                "metrics": {
                    "final_accuracy": float(history.history['accuracy'][-1]),
                    "final_val_accuracy": float(history.history['val_accuracy'][-1]),
                    "final_loss": float(history.history['loss'][-1]),
                    "final_val_loss": float(history.history['val_loss'][-1])
                }
            }
        except Exception as e:
            logger.error(f"Training error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

# Initialize managers
model_manager = ModelManager(Path("./"))
data_processor = DataProcessor(model_manager)
model_trainer = ModelTrainer(model_manager)

@router.post("/upload")
async def upload_and_retrain(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Handle dataset upload and model retraining."""
    try:
        # Validate file type
        if not file.filename.endswith('.zip'):
            raise HTTPException(status_code=400, detail="Only ZIP files are supported")
        
        # Save upload
        zip_path = await data_processor.save_upload(file)
        logger.info(f"File saved to {zip_path}")
        
        # Validate ZIP contents
        is_valid, message = data_processor.validate_zip(zip_path)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Process dataset
        dataset_path = data_processor.process_dataset(zip_path)
        logger.info(f"Dataset processed at {dataset_path}")
        
        # Check if base model exists
        if not model_manager.validate_model_exists("model_densenet"):
            raise HTTPException(
                status_code=404,
                detail="Base model not found. Please ensure 'model_densenet.h5' exists in the models directory"
            )
        
        # Train model
        results = model_trainer.train_model("model_densenet", dataset_path)
        
        # Print the metrics of the retrained model
        metrics = results['metrics']
        logger.info(f"Retrained model metrics:")
        logger.info(f"Final accuracy: {metrics['final_accuracy']}")
        logger.info(f"Final validation accuracy: {metrics['final_val_accuracy']}")
        logger.info(f"Final loss: {metrics['final_loss']}")
        logger.info(f"Final validation loss: {metrics['final_val_loss']}")
        
        return {
            "message": "Model retrained successfully",
            "results": results
        }
        
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
