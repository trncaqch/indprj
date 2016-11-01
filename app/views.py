from django.shortcuts import render

# Create your views here.



def index(request):
    context_dict = dict()
    response = render(request,'index.html', context_dict)

    return response
