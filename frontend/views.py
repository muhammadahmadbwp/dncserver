from django.shortcuts import render
from django.contrib.auth import logout


# Create your views here.

def login_page(request):
	if request.user.is_authenticated:
		return render(request, 'frontend/search.html')	
	return render(request, 'frontend/login.html')

def add_vendor(request):
	if request.user.is_authenticated and request.user.is_superuser:
		return render(request, 'frontend/vendor.html', {'user':request.user})
	elif request.user.is_authenticated and not request.user.is_superuser:
		return render(request, 'frontend/search.html', {'user':request.user})
	else:
		return render(request, 'frontend/login.html')

def upload_dnc_file(request):
	if request.user.is_authenticated and request.user.is_superuser:
		return render(request, 'frontend/uploadfile.html', {'user':request.user})
	elif request.user.is_authenticated and not request.user.is_superuser:
		return render(request, 'frontend/search.html', {'user':request.user})
	else:
		return render(request, 'frontend/login.html')

def search_dnc_system(request):
	if request.user.is_authenticated:
		return render(request, 'frontend/search.html', {'user':request.user})
	return render(request, 'frontend/login.html')

def add_dnc_number(request):
	if request.user.is_authenticated:
		return render(request, 'frontend/adddnc.html', {'user':request.user})
	return render(request, 'frontend/login.html')

def add_dialed_dnc_number(request):
	if request.user.is_authenticated:
		return render(request, 'frontend/adddialeddnc.html', {'user':request.user})
	return render(request, 'frontend/login.html')

def search_dialed_dnc_system(request):
	if request.user.is_authenticated:
		return render(request, 'frontend/searchdialeddnc.html', {'user':request.user})
	return render(request, 'frontend/login.html')

def logout_view(request):
	return render(logout(request), 'frontend/login.html')	