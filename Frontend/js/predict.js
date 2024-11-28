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
        formData.append('image', imageUpload.files[0]);
    
        try {
            const response = await fetch('http://127.0.0.1:8000/', {  // Update with your deployed endpoint
                method: 'POST',
                body: formData
            });
    
            if (!response.ok) {
                throw new Error('Prediction request failed');
            }
    
            const result = await response.json();
            if (result.class) {
                predictionResult.textContent = `Prediction: ${result.class}`;
                confidenceScore.textContent = `Confidence: ${result.confidence}%`;
            } else {
                predictionResult.textContent = 'No prediction received';
                confidenceScore.textContent = '';
            }
        } catch (error) {
            console.error('Error:', error);
            predictionResult.textContent = 'Error making prediction';
            confidenceScore.textContent = '';
        }
    });
});
    