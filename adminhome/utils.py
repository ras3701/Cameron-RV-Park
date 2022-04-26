import datetime, pytz

from .models import  Booking

# TODO [Future Work]: Provide the admin an option to update check-in/check-out time.
TIME_ZONE = " CST"
CHECK_IN_TIME = " 4 pm" + TIME_ZONE
CHECK_OUT_TIME = " 12 pm" + TIME_ZONE

def isPreviousBooking(booking_obj):
   return booking_obj.end_time.replace(tzinfo=pytz.utc) < datetime.datetime.now(pytz.timezone('US/Central'))

def isCurrentBooking(booking_obj):
   return booking_obj.start_time.replace(tzinfo=pytz.utc) <= datetime.datetime.now(pytz.timezone('US/Central')) and booking_obj.end_time.replace(tzinfo=pytz.utc) >= datetime.datetime.now(pytz.timezone('US/Central'))

