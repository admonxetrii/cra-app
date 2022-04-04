from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import pytz

# Models
from accounts.models import UserRestaurant
from api.models import Restaurant, RestaurantTable, RestaurantFloorLevel, TableReservationDates

# Global vars
User = get_user_model()
utc = pytz.timezone(zone="Asia/Kathmandu")


# Create your views here.
def restaurant_obj(request):
    user_restaurant_id = request.user.userrestaurant.id
    ur = UserRestaurant.objects.get(id=user_restaurant_id)
    restaurant_obj_id = Restaurant.objects.get(id=ur.restaurant.id)
    return restaurant_obj_id


def signin(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user is not None:
            try:
                if user.is_restaurant_representative:
                    print(user.userrestaurant)
                    login(request, user)
                    return redirect('dashboard')
            except Exception as e:
                print(e)
            messages.add_message(request, messages.ERROR, "You're not authorized !!!")
            return redirect('signin')
        else:
            messages.add_message(request, messages.ERROR, "Your username and password doesn't match !!!")
            return redirect('signin')


def signout(request):
    logout(request)
    messages.add_message(request, messages.ERROR, "You've been logged out!")
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    print(restaurant_obj(request))
    return render(request, 'dashboard.html')


@login_required(login_url='signin')
def tables(request):
    data1 = RestaurantTable.objects.filter(floorLevel__restaurant=restaurant_obj(request))
    data2 = RestaurantFloorLevel.objects.filter(restaurant=restaurant_obj(request))
    context = {
        'table': data1,
        'floor': data2
    }
    return render(request, 'table.html', context)


@login_required(login_url='signin')
def reservations(request):
    restaurant = restaurant_obj(request)
    res = TableReservationDates.objects.filter(table__floorLevel__restaurant=restaurant).order_by(
        'addedTime')
    now = datetime.datetime.now()
    current_datetime = utc.localize(now)
    for r in res:
        rsvp_date = r.startDate
        print(rsvp_date)
        if r.confirmation:
            fourty_five_min = datetime.timedelta(minutes=45)
            print(current_datetime, fourty_five_min)
            rsvp_cancel_time = rsvp_date + fourty_five_min
            if current_datetime > rsvp_cancel_time:
                r.cancelled = True
                r.cancelled_reason = "USER_DIDNT_ARRIVED"
                r.save()
                print("User didn't arrived so cancelled")
        elif not r.cancelled and not r.confirmation:
            thirty_minute = datetime.timedelta(minutes=30)
            print(current_datetime, rsvp_date, thirty_minute)
            rsvp_cancel_time = rsvp_date - thirty_minute
            if current_datetime > rsvp_cancel_time:
                r.cancelled = True
                r.cancelled_reason = "NOT_CONFIRMED_FROM_RESTAURANT"
                r.save()
                print("Not Confirmed")

    current_datetime = utc.localize(now)
    new_reservations = []
    confirmed_reservations = []
    old_reservations = []
    cancelled = []

    openTime = datetime.datetime.strptime(str(restaurant.openingTime), '%H:%M:%S')
    closeTime = datetime.datetime.strptime(str(restaurant.closingTime), '%H:%M:%S')
    difference = int(str(abs(closeTime - openTime)).split(':')[0])

    res = TableReservationDates.objects.filter(table__floorLevel__restaurant=restaurant)
    try:
        for r in res:
            if r.cancelled:
                cancelled.append(r)
            elif r.startDate > current_datetime:
                if r.confirmation:
                    confirmed_reservations.append(r)
                else:
                    maxDate = r.startDate + datetime.timedelta(days=10)
                    fromTime = (r.startDate + datetime.timedelta(hours=5, minutes=45)).strftime('%I:%M %p')
                    toTime = (r.endDate + datetime.timedelta(hours=5, minutes=45)).strftime('%I:%M %p')
                    newR = {
                        'date': r.startDate.strftime('%Y-%m-%d'),
                        'maxDate': str(maxDate).split(" ")[0],
                        'fromTime': fromTime,
                        'toTime': toTime,
                        'reservation': r
                    }
                    new_reservations.append(newR)
            elif r.success:
                old_reservations.append(r)
    except Exception as e:
        print(e)
    floorLevels = RestaurantFloorLevel.objects.filter(restaurant=restaurant)
    tables = RestaurantTable.objects.filter(floorLevel__restaurant=restaurant)
    tables_object = []
    for t in tables:
        print(t)
        data = {
            'id': t.id,
            'table': t
        }
        tables_object.append(data)

    timeRange = []
    for a in range(0, difference + 1):
        timeFormat = openTime + datetime.timedelta(hours=a)
        timeRangeObj = {
            'id': f"TIME_{a}",
            'time': timeFormat.strftime("%I:%M %p"),
            'fullTime': timeFormat
        }
        timeRange.append(timeRangeObj)

    context = {
        'new': new_reservations,
        'old': old_reservations,
        'confirmed': confirmed_reservations,
        'cancelled': cancelled,
        'tables': tables,
        'floorLevel': floorLevels,
        'res': res,
        'timeRange': timeRange,
        'currentTime': now,
        'tableObj': tables_object
    }

    return render(request, 'reservations.html', context)


@login_required(login_url='signin')
def approve_reservation(request, id):
    date = request.POST.get('date')
    fromTime = request.POST.get('fromTime')
    toTime = request.POST.get('toTime')
    table = request.POST.get('table')
    groupSize = request.POST.get('groupSize')
    remarks = request.POST.get('remarks')
    rsvp_obj = TableReservationDates.objects.get(id=id)
    rsvp_obj.confirmation = 1
    rsvp_obj.remarks = remarks
    rsvp_obj.save()
    return redirect('reservations')


@login_required(login_url='signin')
def cancel_reservation(request, id):
    r = TableReservationDates.objects.get(id=id)
    r.cancelled = 1
    r.cancelled_reason = "CANCELLED_BY_RESTAURANT_USER"
    r.save()
    return redirect('reservations')


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        un = request.POST['username']
        ph = request.POST['phonenumber']
        mp = request.POST['mpass']
        m = masterPass.objects.get(id=1)
        p1 = request.POST['password']
        p2 = request.POST['password_repeat']
        if mp == m.password:
            if p1 == p2:
                u = User(username=un, first_name=fn, last_name=ln)
                u.set_password(p1)
                u.save()
                user = User.objects.get(username=un)
                pic = Profilepic(user_id=user.id)
                pic.phonenumber = ph
                pic.save()
                logs = RestoLogs()
                logs.datentime = datetime.now()
                logs.account = un
                logs.activity = "Signed up!!"
                logs.save()
                messages.add_message(request, messages.SUCCESS, "Your account is registered!!!")
                return redirect('signin')
            else:
                messages.add_message(request, messages.ERROR, "Your confirmation password doesn't match!!!")
                return redirect('register')
        else:
            messages.add_message(request, messages.ERROR, "Your master password doesn't match!!!")
            return redirect('register')
