from rest_framework import serializers
from .models import Vendor, DncNumber


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"


class DncNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = DncNumber
        fields = "__all__"


class GetVendorSerializer(serializers.ModelSerializer):

    dnc_list = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = "__all__"

    def get_dnc_list(self, obj):
        queryset = DncNumber.objects.filter(vendor=obj.id)
        return DncNumberSerializer(queryset, many=True).data