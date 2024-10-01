from django.urls import path
from . import views

app_name = 'classify'
urlpatterns = [
    path('', views.classify_image_view, name='classify_image'),
    path('save-to-drive/<str:img_url>/', views.save_to_drive, name='save_to_drive'),
]
