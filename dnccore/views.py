from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Vendor, DncNumber
from .forms import VendorForm


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