from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home.html'),
    path('show/', views.show_emp, name='show_emp'),
    path('edit/<int:pk>', views.edit_emp, name='edit_emp'),
    path('delete/<int:pk>', views.remove_emp, name='remove_emp'),
]