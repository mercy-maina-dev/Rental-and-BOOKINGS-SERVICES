# bookings/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/',            views.book_house,      name='book_house'),
    path('my-bookings/',              views.my_bookings,     name='my_bookings'),
    path('cancel/<int:pk>/',          views.cancel_booking,  name='cancel_booking'),
    path('manage/<int:pk>/',          views.manage_bookings, name='manage_bookings'),
    path('approve/<int:pk>/',         views.approve_booking, name='approve_booking'),
    path('reject/<int:pk>/',          views.reject_booking,  name='reject_booking'),
]
