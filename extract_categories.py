from facebookads.adobjects.targetingsearch import TargetingSearch
params = {
    'type': 'adTargetingCategory',
    'class': 'interests',
}

resp = TargetingSearch.search(params=params)
print(resp)


#https://graph.facebook.com/2.1/search/type=adTargetingCategory&class=interests
#https://graph.facebook.com/2.1/search/type=adTargetingCategory&class=behaviors

'''
try to use requests package

'''
