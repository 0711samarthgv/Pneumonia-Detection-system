from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload'),
    path('result/<int:pk>/', views.result, name='result'),
    path('gallery/', views.gallery, name='gallery'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('api/analyze/', views.api_analyze, name='api_analyze'),
]
