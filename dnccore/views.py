from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser, MultiPartParser, FormParser, FileUploadParser)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Vendor, DncNumber
from .forms import VendorForm
from .serializers import VendorSerializer, DncNumberSerializer, GetVendorSerializer


def vendors(request):
    vendors = Vendor.objects.all()
    context = {'vendors':vendors}
    return render(request, 'dnccore/vendors.html', context)


def vendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    vendor_dncs = DncNumber.objects.filter(vendor=vendor.id)
    return render(request, 'dnccore/single-vendor.html', {'vendor':vendor, 'vendor_dncs':vendor_dncs})


def createVendor(request):
    form = VendorForm()
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('vendors')
    context = {'form':form}
    return render(request, 'dnccore/vendor_form.html', context)


def updateVendor(request, pk):
    vendor = Vendor.objects.get(id =pk)
    form = VendorForm(instance=vendor)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid:
            form.save()
            return redirect('vendors')
    context = {'form':form}
    return render(request, 'dnccore/vendor_form.html', context)


def deleteVendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendors')
    context = {'object':vendor}
    return render(request, 'dnccore/delete_template.html', context)


class VendorViewSet(viewsets.ViewSet):

    parser_classes = [JSONParser, MultiPartParser, FormParser, FileUploadParser]
    permission_classes = [AllowAny]

    def get_queryset(self, request):
        queryset = Vendor.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = VendorSerializer(queryset, many=True)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({"data":data, "success":True, "message":"vendor created successfully"}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = self.get_queryset(request).get(pk=pk)
        serializer = VendorSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({"data":data, "success":True, "message":"vendor updated successfully"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(request).get(pk=pk)
        serializer = GetVendorSerializer(queryset)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.get_queryset(request).get(pk=pk).delete()
        return Response({"data":[], "success":True, "message":"vendor deleted successfully"}, status=status.HTTP_200_OK)


class DncNumberViewSet(viewsets.ViewSet):

    parser_classes = [JSONParser, MultiPartParser, FormParser, FileUploadParser]
    permission_classes = [AllowAny]

    def get_queryset(self, request):
        queryset = DncNumber.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = DncNumberSerializer(queryset, many=True)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = DncNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({"data":data, "success":True, "message":"dnc created successfully"}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = self.get_queryset(request).get(pk=pk)
        serializer = DncNumberSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({"data":data, "success":True, "message":"dnc updated successfully"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(request).get(pk=pk)
        serializer = DncNumberSerializer(queryset)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.get_queryset(request).get(pk=pk).delete()
        return Response({"data":[], "success":True, "message":"dnc deleted successfully"}, status=status.HTTP_200_OK)