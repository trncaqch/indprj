from django.shortcuts import render
import csv
import pandas
import os
from django.conf import settings as st
# Create your views here.



def index(request):
    context_dict = dict()
    response = render(request,'index.html', context_dict)

    return response

	
def guidelines(request):
    context_dict = dict()
    response = render(request, 'guidelines.html', context_dict)
    return response

def platform(request):
    context_dict = dict()
    response = render(request, 'platform.html', context_dict)
    return response

def google(request):
    context_dict = dict()
    df = pandas.read_csv(st.BASE_DIR+'\\googleAdCategories\\affinity_categories.csv')
    context_dict['googleAdAffinity']=df['Category']
    #print df['Category']
    #print context_dict['googleAdAffinity'][0]
    response = render(request, 'google_platform.html', context_dict)
    return response

def facebook(request):
    context_dict = dict()
    response = render(request, 'facebook_platform.html', context_dict)
    return response

def get_recommendations(request):
    context_dict = dict()
    response = render(request, 'recommendations.html', context_dict)
    return response

