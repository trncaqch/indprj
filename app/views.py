from django.shortcuts import render
import csv
import pandas
import os
import numpy
import math
import unicodedata
import datetime

from django.conf import settings as st
from treelib import Node, Tree

from django.contrib.auth import logout, authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Session

from app.forms import UserForm, SessionForm
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
entsMatrixW2v = pandas.read_csv(st.BASE_DIR+'/matrix_ents_w2v.csv', index_col='category')

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
def match_selection_top(selection, platform):
    selection = selection.split(";")
    mapping = []
    matrixSelected = entsMatrixW2v

    #may be changed for visualization tool if ever implemented 
    #show which category links to which ones
    print selection
    mapDictionary = {}
    if platform=='google':
        for selectedCat in selection:
            n=0
            nselectedCat = unicodedata.normalize('NFKD', selectedCat).encode('ascii','ignore')#gets rid of 'u/'
            recommendedTagsList = []
            mapDictionary[nselectedCat] = []
            while n<10: #change to get top n tags
                maxCosine=0.0
                maxCurrentTag=""
                for fbCat in matrixSelected.index:
                    if matrixSelected[nselectedCat][fbCat]>maxCosine and fbCat not in mapDictionary[nselectedCat]: #and not in recommendedTagsList
                        #print (maxCosine,matrixSelected[nselectedCat][fbCat],fbCat,nselectedCat)
                        formerMaxTag = (maxCurrentTag+'.')[:-1] 
                        maxCosine=matrixSelected[nselectedCat][fbCat]
                        maxCurrentTag=fbCat

                #print (selectedCat,maxCurrentTag)
                #print maxCurrentTag
                mapDictionary[nselectedCat] += [maxCurrentTag]
                #print mapDictionary[nselectedCat]
                
                n+=1

    elif platform=='facebook':
        for selectedCat in selection:
            n=0
            nselectedCat = unicodedata.normalize('NFKD', selectedCat).encode('ascii','ignore')
            mapDictionary[nselectedCat] = []
            while n<10: #change to get top n tags
                maxCosine=0.0
                maxCurrentTag=""
                for ggCat in matrixSelected.columns:
                    if matrixSelected[ggCat][nselectedCat]>maxCosine and ggCat not in mapDictionary[nselectedCat]:
                        #print (maxCosine,matrixSelected[ggCat][nselectedCat],ggCat,nselectedCat)
                        formerMaxTag = (maxCurrentTag+'.')[:-1]
                        maxCosine=matrixSelected[ggCat][nselectedCat]
                        maxCurrentTag=ggCat

                #print (selectedCat,maxCurrentTag)
                if [maxCurrentTag] not in mapping:
                    mapping.append([maxCurrentTag])

                    mapDictionary[nselectedCat] += [maxCurrentTag]
                n+=1
    else:
        mapping = []
    #print mapDictionary
    #print mapping
    context_dict['mapDict'] = mapDictionary
    context_dict['recommendations']=mapping



listOfGoogleCsv = ["affinity_categories.csv","productsservices.csv","in-market_categories.csv"]

GcategoryList = []

GoogleDf = pandas.DataFrame()

#gets all the google categories from all google .csv
for f in listOfGoogleCsv:
    currentDf = pandas.read_csv(st.BASE_DIR+'/googleAdCategories/'+f)
    GoogleDf = GoogleDf.append(currentDf, ignore_index=True)



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
    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
    print context_dict['logged_in']
    response = render(request,'index.html', context_dict)
    return response
	
def guidelines(request):

    response = render(request, 'guidelines.html', context_dict)
    return response

def platform(request):
    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
    response = render(request, 'platform.html', context_dict)
    return response

def past_sessions(request):
    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
    user =  User.objects.get(username = request.user.username)
    Sessions = Session.objects.filter(user=user)
    #print Session.objects.filter(user = user)
    print Session.objects.all()
    response = render(request, 'session.html', context_dict)
    return response


def session(request, session_id):
    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
    response = render(request, 'session.html', context_dict)
    return response


def google(request):
    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
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
    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
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
    saved = False
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        session_form = SessionForm(data=request.POST)
        print 'request is post'
        user =  User.objects.get(username = request.user.username)
        if session_form.is_valid():
            # Save the user's form data to the database.
            session = session_form.save(commit=False)
            
            session.user = user
            session.selected_categories = context_dict['selection']
            session.recommended_categories = context_dict['recommendations']
            session.platform_used = context_dict['platform_used']
            session.session_id = 1
            session.date = datetime.datetime.now()
            session.save()
            context_dict['saved'] = True
            print 'session form is valid'
            response = render(request, 'recommendations.html', context_dict)
            return response
        else:
            print session_form.errors
    else:
        session_form = SessionForm()
    

    if request.user.username!='':
        context_dict['logged_in']=True
    else:
        context_dict['logged_in']=False
        response = render(request, 'login.html', {})
        return response
    match_selection_top(context_dict['selection'], context_dict['platform_used'])
    #print context_dict
    if context_dict['logged_in']==True:
        username = str(request.user.username)
        reco = context_dict['recommendations']
        selection = context_dict['selection'].split(";")
        userDf = pandas.DataFrame(columns=['selection', 'recommendations'],data=None, index=range(len(selection))*10)
        mapDict = context_dict['mapDict']
        n=0
        for selec in mapDict.keys():
            for rec in mapDict[selec]:
                userDf['selection'][n] = selec
                userDf['recommendations'][n] = rec
                n+=1
        userDf.to_csv(username+'.csv')
        '''
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
        '''
    frows = []
    jsRecoInput = mapDict
    for sel in mapDict.keys():
        #print (sel,jsRecoInput[sel], type(jsRecoInput[sel]))
        '''if not isinstance(jsRecoInput[sel], basestring):
            print sel
            jsRecoInput[sel]=''
        '''
        for recommendation in jsRecoInput[sel]:
            
            frows.append([sel]+[recommendation])
    #print frows
    listOfElements = []
    #sorting array in [[x,a],[x,b]] to be form where x is the selection
    for tuple in frows:
        if context_dict['platform_used']=='google':
            ggCat = tuple[0]
            fbCat = tuple[1]
            element = [ggCat]+[fbCat]
        else:
            ggCat = tuple[1]
            fbCat = tuple[0]
            element = [fbCat]+[ggCat]
        cosine = entsMatrixW2v[ggCat][fbCat]
        element+=[cosine]
        listOfElements.append(element)
    context_dict['reco_map']=listOfElements

    session_form = SessionForm()
    context_dict['session_form']=session_form
    context_dict['saved'] = saved



    
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
        #profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            '''
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            '''
            print 'views: user profile created'
            
            
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


