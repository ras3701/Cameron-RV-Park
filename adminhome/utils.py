import datetime, pytz

from .models import  Booking

# TODO [Future Work]: Provide the admin an option to update check-in/check-out time.
TIME_ZONE = " CST"
CHECK_IN_TIME = " 16:00"
CHECK_OUT_TIME = " 12:00"
PYTZ_TIMEZONE = "US/Central"

def isPreviousBooking(booking_obj):
   return booking_obj.end_time.replace(tzinfo=pytz.utc) < datetime.datetime.now(pytz.timezone(PYTZ_TIMEZONE))

def isCurrentBooking(booking_obj):
   return booking_obj.start_time.replace(tzinfo=pytz.utc) <= datetime.datetime.now(pytz.timezone(PYTZ_TIMEZONE)) and booking_obj.end_time.replace(tzinfo=pytz.utc) >= datetime.datetime.now(pytz.timezone(PYTZ_TIMEZONE))

