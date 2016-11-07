from django.shortcuts import render

# Create your views here.

def index(request):
    context_dict = dict()
    response = render(request,'index.html', context_dict)

    return response

	
def guidelines(request):
    context_dict = dict()
    response = render(request, 'guidelines.html', context_dict)
    return response
'''	
def platform(request):

def google(request):

def facebook(request):

def get_recommendations(request):

'''