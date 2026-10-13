# devices/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Device

from .validators import validate_real_image
from pathlib import Path
from django.core.exceptions import ValidationError

ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SIZE = 2 * 1024 * 1024
MAX_IMAGE = 2 * 1024 * 1024  # 2 MB
MAX_MANUAL = 5 * 1024 * 1024 # 5 MB

# forms.py
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ["serial_number", "name", "image", "manual", "organization", "zone" ]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
    
        if image.size > MAX_SIZE:
            raise ValidationError(
                "La imagen no puede superar 2 MB."
            )
        
    
        suffix = Path(image.name).suffix.lower()
        if suffix not in ALLOWED:
            raise ValidationError("Formato no permitido.")

        validate_real_image(image)
        return image

    def clean_manual(self):
        file = self.cleaned_data.get("manual")
        if file and file.size > MAX_MANUAL:
            raise ValidationError("El documento no puede superar 5 MB.")
        return file

