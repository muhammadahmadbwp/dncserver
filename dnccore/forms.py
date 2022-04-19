from django.forms import ModelForm
from .models import Vendor


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = "__all__"