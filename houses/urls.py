# houses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.house_list,         name='house_list'),
    path('houses/<int:pk>/',    views.house_detail,       name='house_detail'),
    path('houses/add/',         views.house_add,          name='house_add'),
    path('houses/<int:pk>/edit/',   views.house_edit,     name='house_edit'),
    path('houses/<int:pk>/delete/', views.house_delete,   name='house_delete'),
    path('dashboard/landlord/', views.landlord_dashboard,
         name='landlord_dashboard'),
    path('dashboard/tenant/',   views.tenant_dashboard,   name='tenant_dashboard'),
]
