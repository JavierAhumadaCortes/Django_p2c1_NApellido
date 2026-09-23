# organizations/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Organization, Department

# organizations/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            "name",
            "tax_id",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej.: Planta Norte",
            }),
            "tax_id": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise ValidationError(
                "Ingrese al menos 3 caracteres."
            )

        return name

