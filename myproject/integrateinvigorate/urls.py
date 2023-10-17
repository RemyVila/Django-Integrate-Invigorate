"""
URL configuration for integrateinvigorate project.

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
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('all_users/', views.all_users, name='all users'),
    path('my_id/', views.get_my_id, name='get my id'),
    path('daily_input/', views.create_daily_input, name='daily input'),
    path('my_daily_inputs/', views.get_all_daily_input_by_user, name='my daily inputs'),
    path('my_averages_by_hours_slept/', views.get_average_wellbeing_vigor_by_hours_slept, name='my averages by hours slept'),
]
