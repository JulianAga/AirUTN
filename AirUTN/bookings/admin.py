from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION
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
        obj.owner = request.user
        super(AdminProperty, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(AdminProperty, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        property_ct = ContentType.objects.get_for_model(Property)
        log_entries = LogEntry.objects.filter(
            content_type=property_ct,
            user=request.user,
            action_flag=ADDITION
        )
        user_property_ids = [a.object_id for a in log_entries]
        return qs.filter(id__in=user_property_ids)
    

admin.site.register(City)
admin.site.register(Property, AdminProperty)