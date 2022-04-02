from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Global Variables
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
            if user.is_restaurant_representative:
                login(request, user)
                return redirect('dashboard')
            messages.add_message(request, messages.ERROR,
                                 "You're not authorized !!!")
            return redirect('signin')
        else:
            messages.add_message(request, messages.ERROR, "Your username and password doesn't match !!!")
            return redirect('signin')

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
