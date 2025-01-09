"""
URL configuration for ApiStudio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('djadmin/', admin.site.urls),

    # Deepak URLS
    path('', include('api_meta.urls')),
    path('', include('api_models.urls')),
    path('', include('core_api.urls')),
    path('admin/app/', include('admin_application.urls')),
    path('auth/', include('authentication.urls')),
    path('', include('user_master.urls')),
    # Mani URLS
    path('', include('database_connection.urls')),
    path('', include('database_schema.urls')),
    path('', include('cms_page.urls')),
    path('', include('views_app.urls')),
    path('', include('api_jobs.urls')),
]
