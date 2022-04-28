from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser, MultiPartParser, FormParser, FileUploadParser)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Vendor, DncNumber
from .forms import VendorForm
from .serializers import VendorSerializer, DncNumberSerializer, GetVendorSerializer, GetDncNumberSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import action



import csv
import io

import time

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


class AuthUserViewSet(viewsets.ModelViewSet):

    @action(methods=['POST'], permission_classes=[AllowAny], detail=False)
    def login(self, request):
        username = request.data['Username']
        password = request.data['Password']
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"data":[], "success":False, "message":"Invalid username/password. Please try again!"}, status=status.HTTP_200_OK)
        login(request, user)
        queryset = User.objects.get(username=user)
        data = {
                'id': str(queryset.id),
                'user': str(queryset.username),
                'is_admin': str(queryset.is_superuser)
            }
        return Response({"data":data, "success":True, "message":"user logged in successfully"}, status=status.HTTP_200_OK)


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
        vendor_id = self.request.query_params.get('vendor_id', None)
        search_dnc_num = self.request.query_params.get('search_dnc_num', None)
        queryset = DncNumber.objects.all()
        if vendor_id != '' and vendor_id is not None:
            queryset = queryset.filter(vendor = vendor_id)        
        if search_dnc_num != '' and search_dnc_num is not None:
            queryset = queryset.filter(dnc_number__icontains = search_dnc_num)
        return queryset

    def list(self, request):
        vendor_id = self.request.query_params.get('vendor_id', None)
        search_dnc_num = self.request.query_params.get('search_dnc_num', None)
        if vendor_id != '' and vendor_id is not None and search_dnc_num != '' and search_dnc_num is not None:
            queryset = DncNumber.objects.filter(vendor = vendor_id, dnc_number__icontains = search_dnc_num)
            serializer = GetDncNumberSerializer(queryset, many=True)
            data = serializer.data
            return Response({"data":data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)
        return Response({"data":[], "success":True, "message":"no data found"}, status=status.HTTP_200_OK)

    def create(self, request):
        file = request.FILES['dnc_num_file']
        file = file.read().decode('ISO-8859-1')
        reader = csv.DictReader(io.StringIO(file))
        data = []
        error_data = []
        st = time.time()
        for n, line in enumerate(reader):
            line['dnc_number'] = line['Phone'].strip()
            if len(line['dnc_number']) > 10:
                error_data.append({"message":f"phone number {line['dnc_number']} at line {n+2} exceeded the set limit"})
                continue
            line['vendor'] = request.data['vendor_id']
            line.pop('Phone')
            data.append(DncNumber(dnc_number=line['dnc_number'], vendor_id=line['vendor']))
        et = time.time()
        print('loop', et-st)
        st = time.time()
        DncNumber.objects.bulk_create(data)
        et = time.time()
        print('save', et-st)
        # st = time.time()
        # serializer = DncNumberSerializer(data=data, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # et = time.time()
        # print('save', et-st)
        # data = serializer.data
        return Response({"data":error_data, "success":True, "message":"dnc created successfully"}, status=status.HTTP_200_OK)

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