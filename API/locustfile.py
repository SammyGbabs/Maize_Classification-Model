from locust import HttpUser, task, between
import os

class ModelTestUser(HttpUser):
    # Wait time between requests (in seconds)
    wait_time = between(1, 2)

    @task
    def test_prediction_endpoint(self):
        # Path to the image you want to upload
        image_path = './Corn_Blight.jpeg'

        # Ensure the image file exists before sending
        if os.path.exists(image_path):
            # Open the image file in binary mode
            with open(image_path, 'rb') as image_file:
                # Prepare the file as multipart/form-data
                files = {'file': (image_path, image_file, 'image/jpeg')}  # Adjust the MIME type as needed (e.g., image/png)

                # Send POST request to the predict endpoint with the image file
                response = self.client.post("/predict", files=files)

                # Log the response from the server
                print(response.text)
        else:
            print(f"Image file not found at {image_path}")
