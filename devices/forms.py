# devices/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Device

from .validators import validate_real_image
from pathlib import Path
from django.core.exceptions import ValidationError

ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SIZE = 2 * 1024 * 1024


# forms.py
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ["serial_number", "name", "image", "organization", "zone" ]

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
