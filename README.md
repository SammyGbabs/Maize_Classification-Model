# Maize_Classification-Model
---

# **Maize Disease Detection Web Application**

## **Project Description**

This project is a web application designed to assist in identifying and managing maize leaf diseases through AI-driven predictions. The application is **dockerized** for easy deployment and provides the following features:

1. **Disease Prediction**  
   - Users can upload maize leaf images, and the system predicts the disease affecting the leaf using a pre-trained machine learning model.

2. **Model Retraining**  
   - Users can upload bulk data (ZIP files of categorized images) to retrain the existing model with their dataset. This ensures the model adapts to new data and remains accurate.

3. **Data Visualizations**  
   - A dedicated page displays various interactive visualizations based on the dataset, with key insights and interpretations.

4. **Model Download**  
   - Users can download the retrained model for their use.

5. **Evaluation Metrics**  
   - Detailed metrics for both prediction and retraining processes are displayed.

6. **Performance Testing**  
   - A **flood request simulation** was conducted using **Locust software** to evaluate system performance under heavy load.

The application is built using **HTML**, **CSS**, and **JavaScript** for the frontend, while the backend is developed with **FastAPI**. The machine learning pipeline was designed from scratch, including scaling and monitoring on a cloud platform.

---

## **Demo Video**

Watch a detailed demonstration of the project in action:  
[YouTube Demo](https://youtu.be/EZy92JYyAjk)  
---

# **Live Links**

## **Live Application**
Access the live application here:  
[Application URL](#)  

## **Live Api Endpoint**

Access the live API Endpoint here:  
[Endpoint URL](https://maize-classification-model.onrender.com)  

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/maize-disease-detection.git
cd maize-disease-detection
```

### **2. Set Up Docker**
Ensure you have Docker installed. Build and run the Docker container:
```bash
# Build the Docker image
docker build -t maize-disease-detection .

# Run the container
docker run -p 8000:8000 maize-disease-detection
```

The application will be accessible at `http://127.0.0.1:8000`.

### **3. Set Up Without Docker (Optional)**
If you prefer to run the application locally without Docker:

#### **Install Dependencies**
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### **Run the Application**
```bash
uvicorn main:app --reload
```

Access the application at `http://127.0.0.1:8000`.

---

## **Features Overview**

### **1. Disease Prediction**
- **Endpoint:** `/predict`
- **Input:** Single image upload.
- **Output:** Predicted disease class and confidence score.

### **2. Model Retraining**
- **Endpoint:** `/retrain/upload`
- **Input:** ZIP file of categorized images.
- **Output:**  
  - Retrained model download link.  
  - Evaluation metrics (loss, accuracy).

### **3. Data Visualizations**
- **Page URL:** `/visualizations`
- **Features:** Interactive plots highlighting dataset insights, such as:  
  - Distribution of disease classes.  
  - Feature correlations.  
  - Trends in image quality or class balance.

### **4. Retrained Model Download**
- **Endpoint:** `/retrain/download-model`

---

## **Flood Request Simulation**

The application’s performance was evaluated under heavy load using **Locust software**. Results include:

- Average response time: *X seconds*  
- Peak concurrent users: *Y users*

Detailed results are available:  
- **CSV File:** [Flood Simulation Results](/Locust_requests.csv)  
- **Visualizations:**  
  ![Flood Simulation](/total_requests_per_second.png)
---

## **Results and Evaluation**

### **Prediction Example**
| Metric       | Value         |  
|--------------|---------------|  
| Predicted Class | Blight |  
| Confidence Score | 58.4% |  

### **Retraining Example**
| Metric   | Value   |  
|----------|---------|  
| Loss     | 0.56    |  
| Accuracy | 83%     |  

---

## **Contributing**

Contributions are welcome! Feel free to open issues or submit pull requests for improvements and new features.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

---

Let me know if further modifications are needed! 🚀
