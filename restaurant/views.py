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
    restaurant = restaurant_obj(request)
    data1 = RestaurantTable.objects.filter(floorLevel__restaurant=restaurant)
    data2 = RestaurantFloorLevel.objects.filter(restaurant=restaurant)
    endTime = str(datetime.datetime.now()).split(" ")[0] + " " + str(restaurant.closingTime)
    endDate = utc.localize(datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S'))
    current_time = utc.localize(datetime.datetime.now() + datetime.timedelta(minutes=30))
    today_rsvp = TableReservationDates.objects.filter(confirmation=True, cancelled=False, endDate__lt=endDate).order_by(
        'startDate')
    context = {
        'table': data1,
        'floor': data2,
        'rsvp': today_rsvp,
        'current_time': current_time
    }
    return render(request, 'table.html', context)

@login_required(login_url='signin')
def reservation_release(request, id):
    rsvp = TableReservationDates.objects.get(id=id)
    table = RestaurantTable.objects.get(id=rsvp.table.id)
    if rsvp.table.isOccupied:
        table.isOccupied = False
        rsvp.tableReleased = True
        rsvp.modifiedTime = utc.localize(datetime.datetime.now())
        rsvp.save()
        table.save()
        messages.add_message(request, messages.SUCCESS, f"Table {table.tableName} is released!!!")
    else:
        messages.add_message(request, messages.ERROR, "Table cannot be released!!!")
    return redirect('table')


@login_required(login_url='signin')
def reservations_accept(request, id):
    rsvp = TableReservationDates.objects.get(id=id)
    table = RestaurantTable.objects.get(id=rsvp.table.id)
    if not rsvp.table.isOccupied:
        table.isOccupied = True
        rsvp.success = True
        rsvp.modifiedTime = utc.localize(datetime.datetime.now())
        rsvp.save()
        table.save()
        messages.add_message(request, messages.SUCCESS, "Table's reservation is accepted!!!")
    else:
        messages.add_message(request, messages.ERROR, "Table is currently occupied, release it first!!!")
    return redirect('table')


@login_required(login_url='signin')
def reservations(request):
    restaurant = restaurant_obj(request)
    res = TableReservationDates.objects.filter(table__floorLevel__restaurant=restaurant).order_by(
        'addedTime')
    now = datetime.datetime.now()
    current_datetime = utc.localize(now)
    for r in res:
        rsvp_date = r.startDate
        if r.confirmation and not r.cancelled:
            fourty_five_min = datetime.timedelta(minutes=45)
            print(current_datetime, fourty_five_min)
            rsvp_cancel_time = rsvp_date + fourty_five_min
            if current_datetime > rsvp_cancel_time:
                if r.success:
                    continue
                r.cancelled = True
                r.cancelled_reason = "USER_DIDNT_ARRIVED"
                r.save()
                print(r.table.tableName, "User didn't arrived so cancelled")
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
    success_reservation = []
    cancelled = []

    openTime = datetime.datetime.strptime(str(restaurant.openingTime), '%H:%M:%S')
    closeTime = datetime.datetime.strptime(str(restaurant.closingTime), '%H:%M:%S')
    difference = int(str(abs(closeTime - openTime)).split(':')[0])

    res = TableReservationDates.objects.filter(table__floorLevel__restaurant=restaurant)
    try:
        for r in res:
            if r.cancelled:
                cancelled.append(r)
            elif r.tableReleased:
                success_reservation.append(r)
            elif r.startDate > current_datetime:
                maxDate = datetime.datetime.now() + datetime.timedelta(days=10)
                fromTime = (r.startDate + datetime.timedelta(hours=5, minutes=45)).strftime('%I:%M %p')
                toTime = (r.endDate + datetime.timedelta(hours=5, minutes=45)).strftime('%I:%M %p')
                newR = {
                    'date': r.startDate.strftime('%Y-%m-%d'),
                    'minDate': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'maxDate': str(maxDate).split(" ")[0],
                    'fromTime': fromTime,
                    'toTime': toTime,
                    'table': r.table.tableName,
                    'reservation': r
                }
                if r.confirmation:
                    confirmed_reservations.append(newR)
                else:
                    new_reservations.append(newR)
    except Exception as e:
        print(e)
    floorLevels = RestaurantFloorLevel.objects.filter(restaurant=restaurant)
    tables = RestaurantTable.objects.filter(floorLevel__restaurant=restaurant)
    tables_object = []
    for t in tables:
        data = {
            'id': t.id,
            'table': t.tableName,
            'seatCap': t.seatCapacity,
        }
        tables_object.append(data)

    rsvp_obj = []
    for r in res:
        if not r.cancelled:
            res_obj = {
                'id': int(r.id),
                'cancelled': int(r.cancelled),
                'confirmation': int(r.confirmation),
                'endDate': r.endDate.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                'table': r.table.id,
                'startDate': r.startDate.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                'success': int(r.success),
                'released': int(r.tableReleased)
            }
            rsvp_obj.append(res_obj)

    timeRange = []
    for a in range(0, difference + 1):
        timeFormat = openTime + datetime.timedelta(hours=a)
        timeRangeObj = {
            'id': a + 1,
            'time': timeFormat.strftime("%I:%M %p"),
            'hour': int(timeFormat.strftime(("%H"))),
            'min': int(timeFormat.strftime(("%M")))
            # 'fullTime': timeFormat
        }
        timeRange.append(timeRangeObj)

    context = {
        'new': new_reservations,
        'success': success_reservation,
        'confirmed': confirmed_reservations,
        'cancelled': cancelled,
        'tables': tables,
        'floorLevel': floorLevels,
        'res': rsvp_obj,
        'timeRange': timeRange,
        'currentTime': now,
        'tableObj': tables_object
    }

    return render(request, 'reservations.html', context)


@login_required(login_url='signin')
def approve_reservation(request, id):
    modified = int(request.POST.get('modified'))
    remarks = request.POST.get('remarks')
    rsvp_obj = TableReservationDates.objects.get(id=id)
    if modified != 0:
        fromTime = request.POST.get('tmpDate')
        toTime = request.POST.get('toDate')
        table = request.POST.get('table')
        groupSize = request.POST.get('groupSize')
        rsvp_obj.startDate = datetime.datetime.fromtimestamp(int(fromTime) / 1000)
        rsvp_obj.endDate = datetime.datetime.fromtimestamp(int(toTime) / 1000)
        rsvp_obj.table = RestaurantTable.objects.get(id=table)
        rsvp_obj.groupSize = groupSize
    rsvp_obj.confirmation = 1
    rsvp_obj.modifiedTime = datetime.datetime.now()
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
