# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context
from django.shortcuts import render_to_response
from models import *


def homepage(request):
    return render_to_response('home.html')
