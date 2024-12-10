import os
import io
import json

def test_upload_image(client):
    # Mock image file
    file_data = io.BytesIO(b"fake-image-data")
    file_data.name = "test.jpg"

    response = client.post('/upload', data={"file": (file_data, file_data.name)})
    assert response.status_code == 200
    data = response.get_json()
    assert "url" in data
    assert data["message"] == "Image uploaded"

def test_upload_no_file(client):
    response = client.post('/upload')
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No file provided"

def test_predict_skin_type(client, mocker):
    # Mock classify_skin_type function
    mocker.patch('app.utils.classify_skin_type', return_value="Normal")

    mock_image_url = "https://storage.googleapis.com/bucket-divaskin/test.jpg"
    response = client.post('/predict', json={"image_url": mock_image_url})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Prediction successful"
    assert data["result"] == "Normal"

def test_predict_no_url(client):
    response = client.post('/predict', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No image URL provided"

def test_delete_image(client, mocker):
    # Mock delete_from_gcs function
    mocker.patch('app.utils.delete_from_gcs', return_value=None)

    mock_image_url = "https://storage.googleapis.com/bucket-divaskin/test.jpg"
    response = client.delete('/delete', json={"image_url": mock_image_url})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Image deleted successfully"

def test_delete_no_url(client):
    response = client.delete('/delete', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No image URL provided"
