from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import City, Property, ReservationDate, Reservation


def index(request):
    cities = City.objects.all()
    context = {'cities': cities }
    return render(request, 'bookings/index.html', context)

def hotel_search(request):
    if request.method == 'GET':
        properties = Property.objects.all()
        context = {'properties': properties}
        return render(request, 'bookings/hotel_search.html', context)
    if request.method == 'POST':
        city = request.POST.get('city', False)
        pax = request.POST.get('pax', False)
        # date-begin = request.POST.get('depart', False)
        # dateEnd = request.POST.get('return', False)
        properties = Property.objects.all()

        if not city.__eq__('None'):
            properties = properties.filter(city=city)

        if not pax.__eq__('None'):
            properties = properties.filter(max_pax__gte=pax)

            # properties = properties.filter(ReservationDate=date-begin)

        context = {'properties': properties}
        return render(request, 'bookings/hotel_search.html', context)
