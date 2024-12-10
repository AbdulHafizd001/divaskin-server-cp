from flask import Blueprint, request, jsonify
from .utils import upload_to_gcs, delete_from_gcs, fetch_image
from .model import classify_skin_type

bp = Blueprint('api', __name__)

@bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty file name"}), 400
    
    try:
        file_url = upload_to_gcs(file)
        return jsonify({"message": "Image uploaded", "url": file_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/predict', methods=['POST'])
def predict_skin_type():
    data = request.json
    image_url = data.get('image_url')
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        image_data = fetch_image(image_url)
        result = classify_skin_type(image_data)
        response = {
            "hasil_analisa": f"Anda memiliki tipe kulit {result['skin_type'].lower()}",
            "akurasi": f"{result['accuracy']}%",
            "deskripsi": result['description'],
            "rekomendasi": result['recommendations']
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/delete', methods=['DELETE'])
def delete_image():
    data = request.json
    image_url = data.get('image_url')
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        delete_from_gcs(image_url)
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
