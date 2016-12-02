from django.shortcuts import render
import csv
import pandas
import os
from django.conf import settings as st
from treelib import Node, Tree

# Create your views here.


#This part works solely with Google ad categories
Gdf = pandas.read_csv(st.BASE_DIR+'/googleAdCategories/affinity_categories.csv')

Gtree = Tree()
Gtree.create_node("Root", "root")

def adCatSplit(cat):
    toSplit = "root" + cat
    r = toSplit.split('/')
    return r
gOrderedList = []

pathLength = 0

while len(gOrderedList) != len(Gdf['Category']):
    pathLength+=1
    for c in Gdf['Category']:
        ele = adCatSplit(c)
        if len(ele)==pathLength:
            gOrderedList.append(ele[-1])
            #print ele[-1]


for c in Gdf['Category']:
    newNode = adCatSplit(c)
    Gtree.create_node(newNode[-1], newNode[-1], newNode[-2])

def get_children(tree, node):
    ch = list()
    for i in tree.children(node):
        ch.append(i.identifier)
    return ch
#use tree.to_json() and create buttons dynamically with javascript
#print Gtree.to_json()

#This part works with Facebook ad categories
fbTree = Tree()
fbTree.create_node("Root", "root")

FBdf = pandas.read_json(st.BASE_DIR+'/fbAdCategories/fbInterestCategories.json')
FBdf = FBdf['data']

pathLength = 0

fbOrderedList = list() #list is ordered by length of the path

while len(fbOrderedList)!=329: #329 is the total number of categories (use CTRL + F and count the number of "id" instances)
    pathLength+=1
    for i in FBdf:
        if len(i['path'])==pathLength:
            fbOrderedList.append(i)

for c in fbOrderedList:
    if fbTree.contains(c['name']):
        continue
    if len(c['path'])==1:
        fbTree.create_node(c['name'], c['name'], "root")
    else:
        fbTree.create_node(c['name'],c['name'], c['path'][-2])

#for i in orderedList:
    #print i['name']

GcategoryList = []
for cat in Gdf.Category:
    GcategoryList.append([cat])

fbCategoryList = []
for 


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
    df = pandas.read_csv(st.BASE_DIR+'/googleAdCategories/affinity_categories.csv')
    context_dict['googleAdAffinity']=GcategoryList
    d = dict()
	
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

