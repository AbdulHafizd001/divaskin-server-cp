import tensorflow as tf
import numpy as np
from PIL import Image
import logging
logging.basicConfig(level=logging.DEBUG)


# Load model globally to avoid reloading
model = tf.keras.models.load_model("model/model.h5")

# Rekomendasi produk berdasarkan tipe kulit
product_recommendations = {
    "Dry": {
        "description": (
            "Kulit kering membutuhkan pelembab yang kaya akan kandungan seperti shea butter atau ceramide. "
            "Berikut adalah rekomendasi produk skincare yang bisa kamu coba untuk membuat kulitmu lebih sehat:"
        ),
        "products": {
            "Facial Wash": {
                "name": "Cetaphil Gentle Skin Cleanser",
                "link": "https://tokopedia.link/BmGh4DRdaPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/dry/Cetaphil%20Gentle%20Skin%20Cleanser.png" 
            },
            "Moisturizer": {
                "name": "Hada Labo Gokujyun Ultimate Moisturizing Lotion",
                "link": "https://tokopedia.link/gIjh1zFdaPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/dry/Hada%20Labo%20Gokujyun%20Ultimate%20Moisturizing%20Lotion.png"
            },
            "Sunscreen": {
                "name": "Skin Aqua UV Moisture Milk SPF 50+ PA+++",
                "link": "https://tokopedia.link/SLH3YxIdaPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/dry/Skin%20Aqua%20UV%20Moisture%20Milk%20SPF%2050%2B%20PA%2B%2B%2B.png"
            }
        }
    },
    "Normal": {
        "description": (
            "Kulit normal cukup menggunakan produk yang ringan untuk menjaga keseimbangan alami. "
            "Berikut adalah rekomendasi produk skincare yang bisa kamu coba untuk membuat kulitmu lebih sehat:"
        ),
        "products": {
            "Facial Wash": {
                "name": "Senka Perfect Whip",
                "link": "https://tokopedia.link/tJos65TdaPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/normal/Senka%20Perfect%20Whip.png"
            },
            "Moisturizer": {
                "name": "Safi Age Defy Day Cream",
                "link": "https://tokopedia.link/FmL362YdaPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/normal/Safi%20Age%20Defy%20Day%20Cream.png"
            },
            "Sunscreen": {
                "name": "Wardah UV Shield Aqua Fresh Essence SPF 50 PA++++",
                "link": "https://tokopedia.link/ToJCKR1daPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/normal/Wardah%20UV%20Shield%20Aqua%20Fresh%20Essence%20SPF%2050%20PA%2B%2B%2B%2B.png"
            }
        }
    },
    "Oily": {
        "description": (
            "Kulit berminyak bisa diatasi dengan produk yang mengandung niacinamide atau zinc untuk mengontrol produksi minyak. "
            "Berikut adalah rekomendasi produk skincare yang bisa kamu coba untuk membuat kulitmu lebih sehat:"
        ),
        "products": {
            "Facial Wash": {
                "name": "Some By Mi AHA BHA PHA 30 Days Miracle Acne Clear Foam",
                "link": "https://tokopedia.link/ZOQbGY4daPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/oily/Some%20By%20Mi%20AHA%20BHA%20PHA%2030%20Days%20Miracle%20Acne%20Clear%20Foam.png"
            },
            "Moisturizer": {
                "name": "Azarine Oil-Free Brightening Daily Moisturizer",
                "link": "https://tokopedia.link/9AAWVR6daPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/oily/Azarine%20Oil-Free%20Brightening%20Daily%20Moisturizer.png"
            },
            "Sunscreen": {
                "name": "Emina Sun Battle SPF 45 PA+++",
                "link": "https://tokopedia.link/AL36RY8daPb",
                "image": f"https://storage.googleapis.com/bucket-divaskin/skincare/oily/Emina%20Sun%20Battle%20SPF%2045%20PA%2B%2B%2B.png"
            }
        }
    }
}

def classify_skin_type(image_data):
    img = Image.open(image_data).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    classes = ["Dry", "Normal", "Oily"]
    skin_type = classes[np.argmax(prediction)]

    # Akurasi
    accuracy = round(np.max(prediction) * 100, 2)

    # Return hasil analisa, deskripsi, dan rekomendasi produk
    return {
        "skin_type": skin_type,
        "accuracy": accuracy,
        "description": product_recommendations[skin_type]["description"],
        "recommendations": product_recommendations[skin_type]["products"]
    }
