from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vendor_view', views.VendorViewSet, basename='vendor-api')

router.register(r'dncnumber_view', views.DncNumberViewSet, basename='dncnumber-api')

router.register(r'userauth', views.AuthUserViewSet, basename='authuser-api')

urlpatterns = [
    path('api/', include(router.urls)),

    # path('', views.vendors, name='vendors'),

    # path('vendor/<str:pk>/', views.vendor, name='vendor'),

    # path('create-vendor/', views.createVendor, name='create-vendor'),

    # path('update-vendor/<str:pk>/', views.updateVendor, name='update-vendor'),

    # path('delete-vendor/<str:pk>/', views.deleteVendor, name='delete-vendor')
]