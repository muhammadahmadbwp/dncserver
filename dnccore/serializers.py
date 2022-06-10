from rest_framework import serializers
from .models import Vendor, DncNumber, DialedDncNumber


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"


class DncNumberSerializer(serializers.ModelSerializer):

    dnc_number = serializers.CharField(min_length=10, max_length=10)

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


class GetDncNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = DncNumber
        fields = "__all__"
        depth = 1


class DialedDncNumberSerializer(serializers.ModelSerializer):

    dnc_number = serializers.CharField(min_length=10, max_length=10)

    class Meta:
        model = DialedDncNumber
        fields = "__all__"


class GetDialedDncNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = DialedDncNumber
        fields = "__all__"
        depth = 1