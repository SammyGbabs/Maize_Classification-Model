document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const datasetUpload = document.getElementById('datasetUpload');
    const uploadStatus = document.getElementById('uploadStatus');
    const fileName = document.getElementById('fileName');
    const removeFile = document.getElementById('removeFile');
    const retrainButton = document.getElementById('retrainButton');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressStatus = document.getElementById('progressStatus');

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
        }
    });

    // Handle file input change
    datasetUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // Handle file selection
    function handleFile(file) {
        fileName.textContent = file.name;
        uploadStatus.classList.remove('hidden');
        retrainButton.disabled = false;
        progressContainer.classList.add('hidden');
        progressBar.style.width = '0%';
        progressStatus.textContent = '0%';
    }

    // Handle file removal
    removeFile.addEventListener('click', () => {
        datasetUpload.value = '';
        uploadStatus.classList.add('hidden');
        retrainButton.disabled = true;
        progressContainer.classList.add('hidden');
    });

    // Handle retrain button click
    retrainButton.addEventListener('click', async () => {
        // Show progress UI
        progressContainer.classList.remove('hidden');
        retrainButton.disabled = true;

        // Simulate progress (replace with actual API call)
        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            progressBar.style.width = `${progress}%`;
            progressStatus.textContent = `${progress}%`;

            if (progress >= 100) {
                clearInterval(interval);
                // Handle completion
            }
        }, 100);

        // API integration will go here
        // const formData = new FormData();
        // formData.append('dataset', datasetUpload.files[0]);
        // const response = await fetch('API_ENDPOINT', {
        //     method: 'POST',
        //     body: formData
        // });
        // const result = await response.json();
        // Handle the retraining result
    });
});