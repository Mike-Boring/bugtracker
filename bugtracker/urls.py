"""bugtracker URL Configuration

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

from homepage.views import login_view, logout_view, index, add_ticket_view, ticket_detail_view

urlpatterns = [
    path('', index, name="homepage"),
    path('addticket/', add_ticket_view, name="addticketview"),
    path('ticket/<int:ticket_id>/', ticket_detail_view, name="ticketview"),
    path('login/', login_view, name="loginview"),
    path('logout/', logout_view, name="logoutview"),
    path('admin/', admin.site.urls),
]
