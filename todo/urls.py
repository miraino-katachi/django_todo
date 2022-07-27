from django.urls import path
from . import views

urlpatterns = [
    # クラスビュー
    path('', views.TodoList.as_view(), name='list'),
    path('login', views.Login, name='Login'),
    path("logout",views.Logout,name="Logout"),
    path('new', views.TodoCreateView.as_view(), name='new'),
    path('edit/<int:pk>', views.TodoUpdateView.as_view(), name='edit'),
    path('complete', views.complete, name='complete'),
    path('delete', views.delete, name='delete'),
    # 関数ビュー
    # path('', views.home, name='home'),
    # path('new', views.new, name='new'),
]
