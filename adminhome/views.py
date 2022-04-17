import json, requests
from datetime import datetime

from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .forms import ParkingCategoryForm, ParkingSpotForm, HomeForm, CustomUserForm, \
    CustomUserCreationForm, DateRangeForm
import boto3

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import ParkingSpot, ParkingCategory
from .filters import ParkingCatergoryFilter, ParkingSpotFilter


def signout(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    logout(request)
    return redirect("adminhome:index")


def signin(request):
    if request.method == "POST":
        form = CustomUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_staff or request.user.is_superuser:
                    return redirect("adminhome:adminhome")
                return redirect("adminhome:userhome")
    else:
        form = CustomUserForm
    return render(request=request,
                  template_name="adminhome/signin.html",
                  context={"form": form})


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Created New Account: {username}")
            login(request, user)
            messages.info(request, f"you are now logged in as {username}")
            return redirect("adminhome:index")
    else:
        form = CustomUserCreationForm
    return render(request=request,
                  template_name="adminhome/signup.html",
                  context={"form": form})


def createparkingspot(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    if (request.method == "POST"):
        form = ParkingSpotForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminhome:viewoneparkingspot', args=(form.instance.id,)))
        else:
            return render(request=request,
                          template_name="adminhome/createparkingspot.html",
                          context={"form": form})

    form = ParkingSpotForm
    return render(request=request,
                  template_name="adminhome/createparkingspot.html",
                  context={"form": form})


def viewparkingspot(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    parkingspot_list = ParkingSpotFilter(request.GET, queryset=ParkingSpot.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(parkingspot_list.qs, 2)

    try:
        parkingspot_paginated = paginator.page(page)
    except PageNotAnInteger:
        parkingspot_paginated = paginator.page(1)
    except EmptyPage:
        parkingspot_paginated = paginator.page(paginator.num_pages)
    return render(request, "adminhome/viewparkingspot.html", {'parkingspot_paginated': parkingspot_paginated,
                                                              'filter': parkingspot_list})


def viewoneparkingspot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    context = {}
    context["parkingspot"] = ParkingSpot.objects.get(id=pk)
    return render(request, "adminhome/viewoneparkingspot.html", context)


def updateparkingspot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    parkingspot = get_object_or_404(ParkingSpot, id=pk)
    form = ParkingSpotForm(request.POST or None, instance=parkingspot)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('adminhome:viewoneparkingspot', args=(form.instance.id,)))

    else:
        return render(request=request,
                      template_name=f"adminhome/updateparkingspot.html",
                      context={"form": form}
                      )


def deleteparkingspot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    parkingspot = get_object_or_404(ParkingSpot, id=pk)
    context["parkingspot"] = parkingspot

    if request.method == 'POST':
        parkingspot.delete()
        return HttpResponseRedirect(reverse("adminhome:viewparkingspot"))

    return render(request, "deleteparkingspot.html", context=context)


def createparkingcategory(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    if (request.method == "POST"):
        form = ParkingCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminhome:viewoneparkingcategory', args=(form.instance.id,)))
        else:
            return render(request=request,
                          template_name="adminhome/createparkingcategory.html",
                          context={"form": form})

    form = ParkingCategoryForm
    return render(request=request,
                  template_name="adminhome/createparkingcategory.html",
                  context={"form": form})


def viewparkingcategory(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    parkingcategory_list = ParkingCatergoryFilter(request.GET, queryset=ParkingCategory.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(parkingcategory_list.qs, 2)

    try:
        parkingcategory_paginated = paginator.page(page)
    except PageNotAnInteger:
        parkingcategory_paginated = paginator.page(1)
    except EmptyPage:
        parkingcategory_paginated = paginator.page(paginator.num_pages)
    return render(request, "adminhome/viewparkingcategory.html",
                  {'parkingcategory_paginated': parkingcategory_paginated,
                   'filter': parkingcategory_list})


def viewoneparkingcategory(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    context = {}
    context["parkingcategory"] = ParkingCategory.objects.get(id=pk)
    return render(request, "adminhome/viewoneparkingcategory.html", context)


def updateparkingcategory(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    parkingcategory = get_object_or_404(ParkingCategory, id=pk)
    form = ParkingCategoryForm(request.POST or None, instance=parkingcategory)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('adminhome:viewoneparkingcategory', args=(form.instance.id,)))

    else:
        return render(request=request,
                      template_name=f"adminhome/updateparkingcategory.html",
                      context={"form": form}
                      )


def deleteparkingcategory(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    parkingcategory = get_object_or_404(ParkingCategory, id=pk)
    context["parkingcategory"] = parkingcategory

    if request.method == 'POST':
        parkingcategory.delete()
        return HttpResponseRedirect(reverse("adminhome:viewparkingcategory"))

    return render(request, "deleteparkingcategory.html", context=context)


def adminhome(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    return render(request, "adminhome/adminhome.html")


def edithome(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    return render(request, "adminhome/edithome.html",
                  {"form": HomeForm(request.POST or None, extra=get_home_metedata())})


def doedit(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    preview_home_metadata = {}
    preview_home_metadata['about'] = {}
    preview_home_metadata['about']['about_header'] = request.POST['about_header']
    preview_home_metadata['about']['about_body'] = request.POST['about_body']

    preview_home_metadata['ameneties'] = {}
    preview_home_metadata['ameneties']['ameneties_header'] = request.POST['ameneties_header']
    preview_home_metadata['ameneties']['ameneties_body'] = request.POST['ameneties_body']

    preview_home_metadata['contact'] = {}
    preview_home_metadata['contact']['phone'] = request.POST['phone']
    preview_home_metadata['contact']['email'] = request.POST['email']
    preview_home_metadata['contact']['location'] = request.POST['location']

    preview_home_metadata['carousel'] = [{} for i in range(3)]
    for i, c in enumerate(request.POST):
        if (c.startswith('carousel_header')):
            preview_home_metadata['carousel'][int(c.split('_')[-1])]['header'] = request.POST[c]
        if (c.startswith('carousel_body')):
            preview_home_metadata['carousel'][int(c.split('_')[-1])]['body'] = request.POST[c]

    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )

    s3 = session.resource('s3')

    sobj = s3.Object(settings.AWS_BUCKET_NAME, settings.AWS_HOME_METADATA_KEY)

    sobj.put(
        Body=(bytes(json.dumps(preview_home_metadata).encode('UTF-8')))
    )

    for i, c in enumerate(request.FILES):
        s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=('media/%s.jpg' % c), Body=request.FILES[c])

    return HttpResponseRedirect(reverse('adminhome:edithome'))


def index(request):
    return render(request, "adminhome/index.html", {"metadata": get_home_metedata()})


def get_home_metedata():
    return requests.get('https://d1dmjo0dbygy5s.cloudfront.net/home_metadata.json').json()

def userhome(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))
    return render(request, "adminhome/userhome.html")

def editprofile(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))
    return render(request, "adminhome/user_editprofile.html")

def addvehicle(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))
    return render(request, "adminhome/user_addvehicle.html")

def editvehicle(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))
    return render(request, "adminhome/user_editvehicle.html")

def checkavailability(request):
    parking_categories_all = ParkingCategory.objects.all()
    parking_categories_available = []
    start_date = ''
    end_date = ''

    if(request.method == "POST"):
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        for parking_category in parking_categories_all:
            _count = 0
            for parking_spot in parking_category.parking_spot.all():
                bookings = parking_spot.booking.exclude(start_time__date__gt=request.POST['end_date'],).exclude(end_time__date__lt=request.POST['start_date'],)
                if(not bookings.exists()):
                    _count = _count + 1
            if(_count > 0):
                parking_categories_available.append(parking_category)

    form = DateRangeForm
    return render(
                    request, 
                    "adminhome/checkavailability.html", 
                    {
                        'parking_categories_available': parking_categories_available,
                        'form': form,
                        'start_date': start_date,
                        'end_date': end_date,
                    }
                )

def assignslots(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    booking = {
        'start_date' : '2022-04-01',
        'end_date' : '2022-04-20'
    }

    parking_category = {
        'parking_spot' : {
            'booking1' : {
                'start_date': '2022-04-01',
                'end_date': '2022-04-10'
            },
            'booking2' : {
                'start_date': '2022-04-15',
                'end_date': '2022-04-20'
            },
        },
        'parking_spot2' : {
            'booking3' : {
                'start_date': '2022-04-01',
                'end_date': '2022-04-07'
            },
            'booking4' : {
                'start_date': '2022-04-13',
                'end_date': '2022-04-20'
            },
        }
    }

    parking_category2 = {
        'parking_spot' : {
            'booking1' : {
                'start_date': '2022-04-01',
                'end_date': '2022-04-10'
            },
            'booking2' : {
                'start_date': '2022-04-15',
                'end_date': '2022-04-20'
            },
        },
        # 'parking_spot2' : {
        #     'booking3' : {
        #         'start_date': '2022-04-01',
        #         'end_date': '2022-04-07'
        #     },
        #     'booking4' : {
        #         'start_date': '2022-04-13',
        #         'end_date': '2022-04-20'
        #     },
        # }
    }
    
    pc = {}

    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(booking['start_date'], date_format)
    end_date = datetime.strptime(booking['end_date'], date_format)
    twd = (end_date - start_date).days + 1
    
    # for i in range(101):
    #     for ps in parking_category2:
    #         pc[ps + str(i)] = {}
    #         for bs in parking_category[ps]:
    #             pc[ps + str(i)][bs] = {}
    #             b = parking_category[ps][bs]
    #             start_date = datetime.strptime(b['start_date'], date_format)
    #             end_date = datetime.strptime(b['end_date'], date_format)
    #             wd = (end_date - start_date).days + 1
    #             pc[ps + str(i)][bs]['wd'] = (100*wd)/twd
    #             pc[ps + str(i)][bs]['mk'] = True
    
    for ps in parking_category:
        pc[ps] = {}
        for bs in parking_category[ps]:
            pc[ps][bs] = {}
            b = parking_category[ps][bs]
            start_date = datetime.strptime(b['start_date'], date_format)
            end_date = datetime.strptime(b['end_date'], date_format)
            wd = (end_date - start_date).days + 1
            print(b)
            print(wd)
            print(wd/twd)
            pc[ps][bs]['wd'] = (100*wd)/twd
            pc[ps][bs]['mk'] = True

    return render(request, "adminhome/assignslots.html", {'pc' : pc})