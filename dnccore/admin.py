from django.contrib import admin

# Register your models here.
from .models import Vendor, DncNumber

admin.site.register(Vendor)
admin.site.register(DncNumber)
