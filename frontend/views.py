from django.shortcuts import render

# Create your views here.

def login_page(request):
	return render(request, 'frontend/login.html')

def add_vendor(request):
	return render(request, 'frontend/vendor.html')

def upload_dnc_file(request):
	return render(request, 'frontend/uploadfile.html')

def search_dnc_system(request):
	return render(request, 'frontend/search.html')