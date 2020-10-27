from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import City, Property, ReservationDate, Reservation


def index(request):
    cities = City.objects.all()
    context = {'cities': cities }
    return render(request, 'bookings/index.html', context)
