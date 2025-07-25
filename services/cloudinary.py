import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

DEFAULT_IMAGE = os.getenv("DEFAULT_PRODUCT_IMAGE")

def upload_image(file):
    if file:
        result = cloudinary.uploader.upload(file.file)
        return result["secure_url"]
    else:
        # Retorna la imagen por defecto si no hay archivo
        return DEFAULT_IMAGE
