from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, Http404

from .models import City, Property, ReservationDate, Reservation

from datetime import datetime, date


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
        datebegin = request.POST.get('depart', False)
        dateEnd = request.POST.get('return', False)
        properties = Property.objects.all()
        propertiesFiltered = []
        if not city.__eq__('None'):
            properties = properties.filter(city=city)

        if not pax.__eq__('None'):
            properties = properties.filter(max_pax__gte=pax)

        if not datebegin == '' and not dateEnd == '':
            diastotales = days_between(datebegin, dateEnd)
            for property in properties:
                reservation = ReservationDate.objects.all()
                reservation = reservation.filter(property=property,reservation__isnull=True)
                initialindex = get_reservation_index(datebegin,reservation)
                finalindex = get_reservation_index(dateEnd,reservation)
                if initialindex > -1 and finalindex > -1:
                    newreservation = reservation.filter()[initialindex:finalindex]
                    
                    if len(newreservation) == diastotales:
                        propertiesFiltered.append(property)    
                              

        context = {'properties': propertiesFiltered}
        return render(request, 'bookings/hotel_search.html', context)

def hotel_details(request, property_id):
    try:
        requested_property = Property.objects.get(id=property_id)
        service = requested_property.daily_cost * 0.08
    except Property.DoesNotExist as property_dont_exist :
        raise Http404("Not Found") from property_dont_exist
    return render(request, 'bookings/hotel-details.html', {'property': requested_property, 'service': service})

def days_between(d1, d2):
       d1 = datetime.strptime(d1, "%Y-%m-%d")
       d2 = datetime.strptime(d2, "%Y-%m-%d")
       return abs((d2 - d1).days)
     
def get_reservation_index(date,reservationDate):
    a = -1
    for i, e in enumerate(reservationDate):
        if str(e.date) == str(date):
            a = i
    return a  # for not found reservation date

def check_availability(request):
    if request.method == 'POST':
        datetime_start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        datetime_end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        requested_property = Property.objects.get(id=request.POST['property_id'])
        reservation_dates = ReservationDate.objects.filter(property=requested_property.id)
        for reservation_date in reservation_dates:
            if reservation_date.reservation is not None:
                if datetime_start_date <= reservation_date.date <= datetime_end_date:
                    return render(request, 'bookings/no-availability.html')        
        count = 0
        for reservation_date in reservation_dates:
            if datetime_start_date <= reservation_date.date <= datetime_end_date:
                r = Reservation(
                reservation_date=reservation_date,
                property=requested_property,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'])
                r.save()
                reservation_date.reservation = r
                reservation_date.save()
                count = count + 1
        if count == 0:
            return render(request, 'bookings/no-availability.html')
        r.total_amount = r.property.daily_cost * r.property.reservationdate_set.filter(reservation=r).count() *1.08
        r.save()        
        return redirect('bookings:successful_booking', r.id,
        datetime_start_date.year,datetime_start_date.month,datetime_start_date.day,
        datetime_end_date.year,datetime_end_date.month,datetime_end_date.day)

def successful_booking(request, reservation_id,year1,month1,day1,year2,month2,day2):
    
    dateBegin = date(int(year1),int(month1),int(day1))
    dateEnd = date(int(year2),int(month2),int(day2))
    try:
        requested_reservation = Reservation.objects.get(id=reservation_id)
        reservationDates = list(ReservationDate.objects.all())        
        initialindex = get_reservation_index(dateBegin,reservationDates)
        finalindex = get_reservation_index(dateEnd,reservationDates)        
        reservationDates = reservationDates[initialindex:finalindex+1]
        
        dates = []
        for d in reservationDates:
            dates.append(d.date)        
        total = "{:.2f}".format(requested_reservation.total_amount)        
    except Property.DoesNotExist:
        raise Http404("Not Found")
    return render(request, 'bookings/itinerary.html', {'reservation': requested_reservation, 'reservation_dates': dates, 'total_amount': total })