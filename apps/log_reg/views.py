from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    print "##########************"
    return render(request, "log_reg/index.html")

def register(request):
    result = User.objects.validate_and_register(request.POST)
    if result[0] == False:
        context = {
            'result':result[1]
        }
        return render(request, "log_reg/index.html", context)
    if result[0] == True:
        context = {
            'name': result[1],
            'action': "successfully registered!"
        }
        return render(request, "log_reg/index.html", context)

def login(request):
    result = User.objects.validate_and_login(request.POST)
    if result[0] == False:
        context = {
            'result':result[1]
        }
        return render(request, "log_reg/index.html", context)
    if result[0] == True:
        request.session['user_name'] = result[1][0].name
        request.session['user_id'] = result[1][0].id
        return redirect('poke_app:index')

# Create your views here.
