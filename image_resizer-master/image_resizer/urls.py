from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('resize_image/',views.resize_image,name="resize_image"),
    path('resize_bulk/',views.resize_bulk,name="resize_bulk"),
    path('download_images/',views.download_images,name="download_images")
]