from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Global Variables
from accounts.models import UserRestaurant
from api.models import Restaurant, RestaurantTable

restaurant_obj = None
User = get_user_model()


# Create your views here.

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
                user_restaurant_id = user.userrestaurant.id
                ur = UserRestaurant.objects.get(id=user_restaurant_id)
                global restaurant_obj
                restaurant_obj = Restaurant.objects.get(id=ur.restaurant.id)
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
    print(restaurant_obj)
    return render(request, 'dashboard.html')


def tables(request):
    data1 = RestaurantTable.objects.filter(floorLevel__restaurant=restaurant_obj)
    context = {
        'table': data1,
    }
    return render(request, 'table.html', context)


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
