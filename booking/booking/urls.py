"""booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.flatpages.views import flatpage
from main.views import index, RoomsListView, RoomDetailView, ProfileView

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', RoomsListView.as_view(), name='rooms-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('about-us/', flatpage, {'url': '/about-us/'}, name='about'),
    path('contact/', flatpage, {'url': '/contact/'}, name='contact'),
    path('admin/', admin.site.urls),
]
