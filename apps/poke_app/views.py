# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from .models import *
from django.core.urlresolvers import reverse
from django.db.models import Count


def index(request):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('log_reg:index')
    id = request.session['user_id']
    me = User.objects.get(id = request.session['user_id'])
    others = User.objects.all().exclude(id = request.session['user_id'])
    my_pokes = Poke.objects.my_pokes(id)
    pokers = Poke.objects.who_poked_me(id)
    pok = []
    for each in pokers:
        pok.append(User.objects.get(alias = each['poker__alias']))
    print pok, "^^^^^^^^^^^^^^^^^^"
    final = []

    for each in pok:
        d = {}
        count = Poke.objects.filter(poker = each, poked = me).count()
        print count, "==============="
        d['name'] = each.alias
        d['count'] = count
        final.append(d)
        print final
    
    
    # pokers2 = User.objects.all().exclude(id = id)
    # print pokers2, "77777777777777777777"


    # pokers2 = Poke.objects.all().exclude(poker = me)
    # for each in pokers2:
    #     if each.poked == me:
    #         print "ura"
    # print len(pokers2), "(((((00000000000)))))))"




    # print request.session['user_id'], "*******&&&&&&&&"
    context = {
        'others':others,
        'my_pokes':my_pokes,
        'pokers':final
    }
    return render(request, "poke_app/index.html", context)

def logout(request):
    request.session.flush()
    return redirect('log_reg:index')

def poke(request):
    if request.method == 'POST':
        Poke.objects.poke(request.POST)
        return redirect('poke_app:index')

# Create your views here.
