from django.contrib import admin
from .models import Property, ReservationDate, City

class ReservationDateInline(admin.TabularInline):
    model = ReservationDate
    exclude = ['reservation']
    fk_name = 'property'
    max_num = 7

class AdminProperty(admin.ModelAdmin):
    inlines = [ReservationDateInline, ]
    exclude = ['owner']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(AdminProperty, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

admin.site.register(City)
admin.site.register(Property, AdminProperty)
