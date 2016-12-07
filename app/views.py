from django.shortcuts import render
import csv
import pandas
import os
from django.conf import settings as st
from treelib import Node, Tree

from django.contrib.auth import logout, authenticate, login, logout
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required

import django

# Create your views here.


#This part works solely with Google ad categories
Gdf = pandas.read_csv(st.BASE_DIR+'/googleAdCategories/affinity_categories.csv')

entsDf = pandas.read_csv(st.BASE_DIR+'/matrix_ents_modified.csv', index_col='category')


context_dict={}



#ENTS PART
ents_matrix = pandas.read_csv(st.BASE_DIR+'/matrix_ents_modified.csv', index_col='category')

def match_selections(selection):
    selection = selection.split(";")
    mapping = []
    for selectedCat in selection:
        for fbCat in ents_matrix.index:
            if ents_matrix[selectedCat][fbCat]==1:
                if [fbCat] in mapping:
                    continue
                mapping.append([fbCat])
    context_dict['recommendations']=mapping



GaffinityList = []
for cat in Gdf.Category:
    GaffinityList.append([cat])

listOfGoogleCsv = ["affinity_categories.csv","productsservices.csv","in-market_categories.csv"]

GcategoryList = []

GoogleDf = pandas.DataFrame()


for f in listOfGoogleCsv:
    currentDf = pandas.read_csv(st.BASE_DIR+'/googleAdCategories/'+f)
    GoogleDf = GoogleDf.append(currentDf, ignore_index=True)
print GoogleDf


listOfFBCsv = ['fbInterestCategories', 'fbBehaviorsCategories', 
'fbEthnicAffinityCategories', 'fbFamilyStatusesCategories', 
'fbGenerationCategories', 'fbHouseholdCompoCategories',
'fbIncomeCategories', 'fbIndustriesCategories', 
'fbLifeEventsCategories', 'fbNetWorthCategories', 
'fbPoliticsCategories', 'fbUserDeviceCategories']


FacebookDf = pandas.DataFrame()

for f in listOfFBCsv:
    currentDf = pandas.read_csv(st.BASE_DIR+'/fbAdCategories/csv/'+f+'.csv')
    currentDf = currentDf.drop('Unnamed: 0',1)#drop redundant column
    FacebookDf = FacebookDf.append(currentDf, ignore_index=True)


def index(request):
    #context_dict = dict()
    response = render(request,'index.html', context_dict)

    return response
	
def guidelines(request):
    response = render(request, 'guidelines.html', context_dict)
    return response

def platform(request):
    response = render(request, 'platform.html', context_dict)
    return response

def google(request):
    tolist = []
    for i in entsDf.columns:
        tolist.append([i])
    context_dict['googleAdAffinity']=tolist

    if request.method == 'POST':
        if 'selection' in request.POST:
            selection = request.POST['selection']
            context_dict['selection']=selection
            print selection

    response = render(request, 'google_platform.html', context_dict)
    return response

def facebook(request):
    response = render(request, 'facebook_platform.html', context_dict)
    return response

def get_recommendations(request):
    match_selections(context_dict['selection'])
    response = render(request, 'recommendations.html', context_dict)
    return response



def register(request):
    # A boolean value for telling the template whether the registration was successful.
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                django.contrib.auth.login(request, user)
                context_dict['username']=username
                print username
                return render(request, 'index.html', {})
            else:

                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided.
            return render(request, 'login.html', {})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})



@login_required
def user_logout(request):

    logout(request)
    context_dict['username']=""
    return render(request, 'index.html', {})


