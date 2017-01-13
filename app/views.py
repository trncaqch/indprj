from django.shortcuts import render
import csv
import pandas
import os
from django.conf import settings as st
from treelib import Node, Tree

from django.contrib.auth import logout, authenticate, login, logout
from django.contrib.auth.models import User

from app.forms import UserForm
from django.contrib.auth.decorators import login_required

import django

# Create your views here.


#This part works solely with Google ad categories
Gdf = pandas.read_csv(st.BASE_DIR+'/googleAdCategories/affinity_categories.csv')

entsDf = pandas.read_csv(st.BASE_DIR+'/matrix_ents_modified.csv', index_col='category')


context_dict={}

#ENTS PART
ents_matrix = pandas.read_csv(st.BASE_DIR+'/matrix_ents_modified.csv', index_col='category')
entsMatrixCos = pandas.read_csv(st.BASE_DIR+'/matrix_ents_cosine.csv', index_col='category')

'''selects matches and maps each selected option
to another one using binary values'''
def match_sel_bin(selection):
    selection = selection.split(";")
    mapping = []
    for selectedCat in selection:
        for fbCat in ents_matrix.index:
            if ents_matrix[selectedCat][fbCat]==1:
                if [fbCat] in mapping:
                    continue
                mapping.append([fbCat])
    context_dict['recommendations']=mapping

'''
selects matches and maps each option
with another one using the maximum textual cosine similarity rate
'''
def match_sel_cosine(selection, platform):
    selection = selection.split(";")
    mapping = []


    #may be changed for visualization tool if ever implemented 
    #show which category links to which ones
	
	
    if platform=='google':
        for selectedCat in selection:
            n=0
            while n<1:
                maxCosine=0.0
                maxCurrentTag=""
                for fbCat in entsMatrixCos.index:
                    if entsMatrixCos[selectedCat][fbCat]>maxCosine:
                        print (maxCosine,entsMatrixCos[selectedCat][fbCat],fbCat,selectedCat)
                        maxCosine=entsMatrixCos[selectedCat][fbCat]
                        maxCurrentTag=fbCat
                        if [fbCat] in mapping: 
                            continue
                print (selectedCat,maxCurrentTag)
                if [maxCurrentTag] not in mapping:
                    mapping.append([maxCurrentTag])
                n+=1

    elif platform=='facebook':
        for selectedCat in selection:
            n=0
            while n<1:
                maxCosine=0.0
                maxCurrentTag=""
                for ggCat in entsMatrixCos.columns:
                    if entsMatrixCos[ggCat][selectedCat]>maxCosine:
                        print (maxCosine,entsMatrixCos[ggCat][selectedCat],ggCat,selectedCat)
                        maxCosine=entsMatrixCos[ggCat][selectedCat]
                        maxCurrentTag=ggCat
                        if [ggCat] in mapping: 
                            continue
                print (selectedCat,maxCurrentTag)
                if [maxCurrentTag] not in mapping:
                    mapping.append([maxCurrentTag])
                n+=1
    else:
        mapping = []
    context_dict['recommendations']=mapping

#______________
#maybe useless
GaffinityList = []
for cat in Gdf.Category:
    GaffinityList.append([cat])
#______________

listOfGoogleCsv = ["affinity_categories.csv","productsservices.csv","in-market_categories.csv"]

GcategoryList = []

GoogleDf = pandas.DataFrame()

#gets all the google categories from all google .csv
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

#gets all the facebook categories from all facebook .csv
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
    context_dict['platform_used'] = "google"
    tolist = []
    for i in entsDf.columns:
        tolist.append([i])
    ''' 
    put all the categories in a list for the google side table 
    they are going to be the ones to be selected by the user
    '''
    context_dict['googleAdAffinity']=tolist
    '''
    Catching the post request (selected categories) in context
    '''
    if request.method == 'POST':
        if 'selection' in request.POST:
            selection = request.POST['selection']
            context_dict['selection']=selection
            print selection

    response = render(request, 'google_platform.html', context_dict)
    return response

def facebook(request):
    context_dict['platform_used'] = "facebook"
    tolist = []
    for i in entsDf.index:
        tolist.append([i])
    ''' 
    put all the categories in a list for the google side table 
    they are going to be the ones to be selected by the user
    '''
    context_dict['facebookCategories']=tolist
    '''
    Catching the post request (selected categories) in context
    '''
    if request.method == 'POST':
        if 'selection' in request.POST:
            selection = request.POST['selection']
            context_dict['selection']=selection
            print selection

    response = render(request, 'facebook_platform.html', context_dict)
    return response

def get_recommendations(request):
    match_sel_cosine(context_dict['selection'], context_dict['platform_used'])
    print context_dict
    if context_dict['logged_in']==True:
        username = context_dict['username']
        reco = context_dict['recommendations']
        selection = context_dict['selection'].split(";")
        userDf = pandas.DataFrame(columns=['selection', 'recommendations'],data=None, index=range(len(selection)))
        for c in userDf.columns:
            n=0
            if c=='selection':
                for i in selection:
                    userDf[c][n]=i
                    n+=1
            else:
                for i in reco:
                    userDf[c][n]=i
                    n+=1
        userDf.to_csv(username+'.csv')
    response = render(request, 'recommendations.html', context_dict)
    return response



'''
login/register related
'''
def register(request):
    # A boolean value for telling the template whether the registration was successful.
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'registered': registered} )


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
                context_dict['logged_in']=True
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
    context_dict['logged_in']=False
    return render(request, 'index.html', context_dict)


