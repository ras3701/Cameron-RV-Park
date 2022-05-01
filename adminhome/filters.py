from dataclasses import field
from django.forms import DateInput, widgets
import django_filters
from .models import  ParkingCategory, ParkingSpot, Booking, Vehicle
from .forms import DatePickerInput

class ParkingCatergoryFilter(django_filters.FilterSet):
    ps_status = django_filters.BooleanFilter(label='Is Parking Category Active', field_name='is_active')

    class Meta:
        model = ParkingCategory
        fields = ('ps_status',)

class ParkingSpotFilter(django_filters.FilterSet):
    ps_status = django_filters.BooleanFilter(label='Is Parking Spot Active', field_name='is_active')
    parking_cat_name = django_filters.AllValuesFilter(label='Parking Category Name', field_name='parking_category_id__name')

    class Meta:
        model = ParkingSpot
        fields = ('ps_status', 'parking_cat_name',)

class BookingFilter(django_filters.FilterSet):
    parking_spot_name = django_filters.AllValuesFilter(label='Parking Spot Name', field_name='parking_spot_id__name')
    is_lease_signed_by_user = django_filters.BooleanFilter(label='Is Lease Signed by the User', field_name='lease_is_signed_by_user')
    booking_state = django_filters.AllValuesFilter(label='Booking State', field_name='state')
    username = django_filters.CharFilter(label='Username', field_name='vehicle_id__user_id__username')

    class Meta:
        model = Booking
        fields = ('parking_spot_name', 'is_lease_signed_by_user', 'booking_state', 'username',)

class PreviousAndCurrentBookingFilter(django_filters.FilterSet):
    parking_spot_name = django_filters.AllValuesFilter(label='Parking Spot Name', field_name='parking_spot_id__name')
    booking_state = django_filters.AllValuesFilter(label='Booking State', field_name='state')
    username = django_filters.CharFilter(label='Username', field_name='vehicle_id__user_id__username')

    class Meta:
        model = Booking
        fields = ('parking_spot_name', 'booking_state', 'username',)

class AllBookingFilter(django_filters.FilterSet):
    parking_cat_name = django_filters.AllValuesFilter(label='Parking Category Name', field_name='pc_id__name')
    parking_spot_name = django_filters.AllValuesFilter(label='Parking Spot Name', field_name='parking_spot_id__name')
    is_lease_signed_by_user = django_filters.BooleanFilter(label='Is Lease Signed by the User', field_name='lease_is_signed_by_user')
    booking_state = django_filters.AllValuesFilter(label='Booking State', field_name='state')
    username = django_filters.CharFilter(label='Username', field_name='vehicle_id__user_id__username')
    vehicle_name = django_filters.CharFilter(label='Vehicle Name', field_name='vehicle_id__name')
    vehicle_vin = django_filters.CharFilter(label='Vehicle VIN', field_name='vehicle_id__vin')

    start_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), method='filter_start_date', label='Start Date')
    end_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), method='filter_end_date', label='End Date')

    def filter_start_date(self, queryset, name, value):
        return queryset.filter(start_time__gte=value)

    def filter_end_date(self, queryset, name, value):
        return queryset.filter(end_time__lte=value)

    class Meta:
        model = Booking
        fields = ('parking_cat_name', 'parking_spot_name', 'is_lease_signed_by_user', 'booking_state', 'username', 'vehicle_name', 'vehicle_vin', 'start_date', 'end_date',)

class UserBookingFilter(django_filters.FilterSet):
    parking_spot_name = django_filters.AllValuesFilter(label='Parking Spot Name', field_name='parking_spot_id__name')
    vehicle_name = django_filters.CharFilter(label='Vehicle Name', field_name='vehicle_id__name')
    vehicle_vin = django_filters.CharFilter(label='Vehicle VIN', field_name='vehicle_id__vin')

    class Meta:
        model = Booking
        fields = ('parking_spot_name', 'vehicle_name', 'vehicle_vin',)    


class UnverifiedVehiclesFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(label='Username', field_name='user_id__username')

    class Meta:
        model = Vehicle
        fields = ('username',)
