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

    // Button and UI element references
    retrainButton.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent form submission if inside a form
        retrainButton.disabled = true;
        loader.classList.remove('hidden');
        metricsContainer.classList.add('hidden');
        
        try {
            // File validation
            const file = datasetUpload.files[0];
            if (!file) {
                throw new Error('Please select a ZIP file before retraining');
            }

            const allowedTypes = [
                'application/zip',
                'application/x-zip',
                'application/x-zip-compressed',
                'application/octet-stream'
            ];

            const fileExtension = file.name.toLowerCase().split('.').pop();
            if (!allowedTypes.includes(file.type) && fileExtension !== 'zip') {
                throw new Error('Please upload a valid ZIP file');
            }

            const maxSize = 100 * 1024 * 1024; // 100MB in bytes
            if (file.size > maxSize) {
                throw new Error(`ZIP file size exceeds limit of ${maxSize / (1024 * 1024)}MB`);
            }

            console.log('File validation passed:', { name: file.name, size: `${(file.size / (1024 * 1024)).toFixed(2)}MB`, type: file.type, extension: fileExtension });

            const formData = new FormData();
            formData.append('file', file);
            // Log FormData contents
            for (let [key, value] of formData.entries()) {
                console.log(key, value);
            }            
            // Create abort controller for timeout handling
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 180000); // 3-minute timeout

            const response = await fetch('http://127.0.0.1:8000/retrain/upload', {
                method: 'POST',
                body: formData,
                signal: controller.signal,
            });

            // Reset the timeout after the response is received
            clearTimeout(timeoutId);

            // Handle the response
            if (response.ok) {
                const data = await response.json();
                console.log('File uploaded successfully:', data);
                
                const result = await response.json();
                console.log(result);
                
                // Validate response structure
                if (!result.results?.metrics) {
                    throw new Error('Invalid server response format');
                }

                const metrics = result.results.metrics;

                if (metrics.final_loss !== undefined) {
                    lossElement.textContent = metrics.final_loss.toFixed(4);
                }

                if (metrics.final_accuracy !== undefined) {
                    accuracyElement.textContent = `${(metrics.final_accuracy * 100).toFixed(2)}%`;
                }

                if (result.results.model_path) {
                    modelPathElement.textContent = result.results.model_path;
                }

                alert('Model retraining completed successfully!');
                metricsContainer.classList.remove('hidden');
            } else {
                console.error('File upload failed:', response.statusText);
            }
        } catch (error) {
            console.error('Error during file validation or upload:', error);
            alert(error.message);  // Show error message to the user
        } finally {
            retrainButton.disabled = false;
            loader.classList.add('hidden');
        }
    });
});
