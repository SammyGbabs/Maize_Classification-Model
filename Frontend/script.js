// Upload data for retraining
function uploadData() {
    const files = document.getElementById("file-upload").files;
    const formData = new FormData();
    for (let file of files) {
      formData.append("files", file);
    }
  
    fetch("http://your-backend-url/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Data uploaded successfully!");
        console.log(data);
      })
      .catch((error) => console.error("Error:", error));
  }
  
  // Make a prediction
  function makePrediction() {
    const file = document.getElementById("prediction-upload").files[0];
    const formData = new FormData();
    formData.append("file", file);
  
    fetch("http://your-backend-url/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("prediction-result").innerText =
          `Prediction: ${data.prediction}`;
      })
      .catch((error) => console.error("Error:", error));
  }
  
  // Trigger retraining
  function retrainModel() {
    fetch("http://your-backend-url/retrain", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        alert("Model retrained successfully!");
        console.log(data);
      })
      .catch((error) => console.error("Error:", error));
  }
  
  // Visualization (example using Chart.js)
  function renderVisualization() {
    const ctx = document.getElementById("visualization-chart").getContext("2d");
    fetch("http://your-backend-url/visualization-data")
      .then((response) => response.json())
      .then((data) => {
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: data.labels,
            datasets: [{
              label: "Feature Visualization",
              data: data.values,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            }],
          },
        });
      })
      .catch((error) => console.error("Error:", error));
  }
  
  // Call the visualization function
  renderVisualization();
  