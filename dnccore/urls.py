from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendors, name='vendors'),

    path('vendor/<str:pk>/', views.vendor, name='vendor'),

    path('create-vendor/', views.createVendor, name='create-vendor'),

    path('update-vendor/<str:pk>/', views.updateVendor, name='update-vendor'),

    path('delete-vendor/<str:pk>/', views.deleteVendor, name='delete-vendor')
]