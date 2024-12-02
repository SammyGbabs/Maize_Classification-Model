document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const datasetUpload = document.getElementById('datasetUpload');
    const uploadStatus = document.getElementById('uploadStatus');
    const fileName = document.getElementById('fileName');
    const removeFile = document.getElementById('removeFile');
    const retrainButton = document.getElementById('retrainButton');
    const metricsContainer = document.getElementById('metricsContainer');
    const lossElement = document.getElementById('loss');
    const accuracyElement = document.getElementById('accuracy');
    const modelPathElement = document.getElementById('modelPath');
    const loader = document.getElementById('loader');

    // Check if required DOM elements are present
    if (!retrainButton || !metricsContainer || !loader || !uploadArea || !datasetUpload || !uploadStatus || !fileName || !removeFile) {
        console.error('Required DOM elements are missing');
        return;
    }

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
        if (file && file.name.endsWith('.zip')) {
            handleFile(file);
        } else {
            alert("Please upload a valid ZIP file.");
        }
    });

    datasetUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    function handleFile(file) {
        fileName.textContent = file.name;
        uploadStatus.classList.remove('hidden');
        retrainButton.disabled = false;
    }

    removeFile.addEventListener('click', () => {
        datasetUpload.value = '';
        uploadStatus.classList.add('hidden');
        retrainButton.disabled = true;
        metricsContainer.classList.add('hidden');
        loader.classList.add('hidden');
    });

    retrainButton.addEventListener('click', async () => {
        retrainButton.disabled = true;
        loader.classList.remove('hidden');
        metricsContainer.classList.add('hidden');
    
        try {
            const file = datasetUpload.files[0];
            
            if (!file) {
                throw new Error('No file selected');
            }
            
            console.log('File details:', {
                name: file.name,
                size: file.size,
                type: file.type
            });
    
            const formData = new FormData();
            formData.append('file', file);
    
            console.log('Starting upload and retraining...');
            
            const response = await fetch('http://127.0.0.1:8000/retrain/upload', {
                method: 'POST',
                body: formData
            });
    
            if (!response.ok) {
                let errorMessage = 'Upload failed';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (err) {
                    console.error('Error parsing response JSON:', err);
                }
                throw new Error(errorMessage);
            }
    
            const result = await response.json();
            console.log('Retraining successful:', result);
    
            // Update UI with results from the new API structure
            const metrics = result.results.metrics;
            lossElement.textContent = metrics.final_loss.toFixed(4);
            accuracyElement.textContent = `${(metrics.final_accuracy * 100).toFixed(2)}%`;
            modelPathElement.textContent = result.results.model_path;
    
            metricsContainer.classList.remove('hidden');
            alert('Model retraining completed successfully!');
    
        } catch (error) {
            console.error('Error during uploaded or retraining:', error);
            alert(`Error: ${error.message}`);
        } finally {
            retrainButton.disabled = false;
            loader.classList.add('hidden');
        }
    });
});
