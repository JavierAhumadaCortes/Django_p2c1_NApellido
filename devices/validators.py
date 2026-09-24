#devices/validators.py
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

def validate_real_image(image):
    try:
        with Image.open(image) as picture:
            picture.verify()

    except (UnidentifiedImageError, OSError):
        raise ValidationError(
            "El archivo no es una imagen válida."
        )

    finally:
        image.seek(0)

    return image