import uuid
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.vendor_name

class DncNumber(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    dnc_number = models.CharField(max_length=20)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.dnc_number

class DialedDncNumber(models.Model):
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    dnc_number = models.CharField(max_length=20)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)