# devices/models.py
from django.db import models
from core.models import BaseModel

class Device(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="devices",
    )
    zone = models.ForeignKey(
        "organizations.Zone",
        on_delete=models.PROTECT,
        related_name="devices",
    )
    name = models.CharField(max_length=120)
    serial_number = models.CharField(max_length=80, unique=True)
    image = models.ImageField(
        upload_to="devices/%Y/%m/",
        blank=True,
    )
    
    def __str__(self):
        return self.name


class Measurement(BaseModel):
    device = models.ForeignKey(
        "devices.Device",
        on_delete=models.PROTECT,
        related_name="measurements",
    )

    measured_at = models.DateTimeField()

    energy_kwh = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    triggered_alert = models.ForeignKey(
        "devices.AlertRule",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="measurements",
    )

    class Meta:
        ordering = ("-measured_at",)

        indexes = [
            models.Index(
                fields=["device", "measured_at"],
                name="measurement_device_date_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.device} - "
            f"{self.energy_kwh} kWh - "
            f"{self.measured_at}"
        )
        

class AlertRule(BaseModel):
    name = models.CharField(
        max_length=100
    )

    device = models.ForeignKey(
        "devices.Device",
        on_delete=models.CASCADE,
        related_name="alert_rules",
    )

    threshold_kwh = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.name} - {self.device}"

