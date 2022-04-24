from django.urls import path
from . import views

urlpatterns = [
	path('', views.search_dnc_system, name="search-dnc-system"),

	path('upload-dnc-file', views.upload_dnc_file, name="upload-dnc-file"),

	path('add-vendor', views.add_vendor, name="add-vendor"),
]