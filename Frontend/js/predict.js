document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');
    const predictButton = document.getElementById('predictButton');
    const predictionResult = document.getElementById('predictionResult');
    const confidenceScore = document.getElementById('confidenceScore');

    // Handle drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        }
    });

    // Handle file input change
    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // Handle file preview and button state
    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            imagePreview.classList.remove('hidden');
            predictButton.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Handle predict button click
    predictButton.addEventListener('click', async () => {
        const formData = new FormData();
    
        const file = imageUpload.files[0];
        if (!file) {
            predictionResult.textContent = 'Please upload an image before predicting.';
            return;
        }
    
        formData.append('image', file);
    
        try {
            console.log("Sending image for prediction...");
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                body: formData,
            });
    
            const result = await response.json();
            console.log("Response Data:", result);
    
            // Show results in the result display section
            const resultDisplay = document.getElementById('resultDisplay');
            const predictionResult = document.getElementById('predictionResult');
            const confidenceScore = document.getElementById('confidenceScore');
    
            if (result.prediction) {
                resultDisplay.classList.remove('hidden');
                predictionResult.textContent = `Prediction: ${result.prediction.class}`;
                confidenceScore.textContent = `Confidence: ${(result.prediction.confidence * 100).toFixed(2)}%`;
            } else {
                predictionResult.textContent = 'No prediction received';
                confidenceScore.textContent = '';
            }
        } catch (error) {
            console.error('Error making prediction:', error);
            predictionResult.textContent = 'Error making prediction';
            confidenceScore.textContent = '';
        }
    });    
});
    