"""
URL configuration for aimagestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns

from . import views, settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('classify/', include('image_classification.urls')),
    path('chat/', views.chat_with_bot, name='chat_with_bot'),
    # path('', views.home, name='home'),
    # path('auth/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('auth/', include('accounts.urls')),
    path('', views.home, name='home')
)

# if 'rosetta' in settings.INSTALLED_APPS:
#     urlpatterns += [
#         re_path(r'^rosetta/', include('rosetta.urls'))
#     ]
