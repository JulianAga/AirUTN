from django.conf.urls import url

from . import views

app_name = 'bookings'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/', views.hotel_search, name='hotel_search'),
    url(r'^property/([0-9]+)/$', views.hotel_details, name='hotel_details'),
    url(r'^check_availability/', views.check_availability, name='check_availability'),
    url(r'^reservation/([0-9]+)/$', views.successful_booking, name='successful_booking')
]
