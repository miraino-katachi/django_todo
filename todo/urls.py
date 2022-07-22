from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.Login, name='Login'),
    path("logout",views.Logout,name="Logout"),
    path('new', views.new, name='new'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('complete', views.complete, name='complete'),
    path('delete', views.delete, name='delete'),
]
