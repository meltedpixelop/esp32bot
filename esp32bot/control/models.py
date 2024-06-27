from django.db import models

class ESP32Record(models.Model):
    ip_address = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} at {self.timestamp}"
