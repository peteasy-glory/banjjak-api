"""banjjak_partner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html')),
    path('partner/', include('apiLogin.urls')),
    path('partner/', include('apiHome.urls')),
    path('partner/', include('apiBooking.urls')),
    path('partner/', include('apiShop.urls')),
    path('partner/', include('apiCustomer.urls')),
    path('partner/', include('apiSetting.urls')),
    path('partner/', include('apiPerformance.urls')),
    path('partner/', include('apiEtc.urls')),
]
