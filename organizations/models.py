# organizations/models.py
from django.db import models
from core.models import BaseModel

class Organization(BaseModel):
    name = models.CharField(max_length=150)
    tax_id = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Department(BaseModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="departments",
    )
    name = models.CharField(max_length=100)

class Zone(BaseModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="zones",
    )
    name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name
    
# accounts/models.py
from django.conf import settings

class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="user_profiles",
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.PROTECT,
        related_name="user_profiles",
        null=True,
        blank=True,
    )
    employee_code = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} · {self.organization}"
    