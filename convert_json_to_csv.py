import pandas
import numpy as np
import random


'''
This part converts fbAdCategories.json to .csv with index and category as headers
'''

toConvert = ['fbInterestCategories', 'fbBehaviorsCategories', 'fbEthnicAffinityCategories', 'fbFamilyStatusesCategories', 'fbGenerationCategories', 'fbHouseholdCompoCategories','fbIncomeCategories', 'fbIndustriesCategories', 'fbLifeEventsCategories', 'fbNetWorthCategories', 'fbPoliticsCategories', 'fbUserDeviceCategories']



for jsonFile in toConvert:
    df = pandas.read_json('fbAdCategories/json/'+jsonFile+'.json')
    df = df['data']
    pathLength = 0
    fbCsv = pandas.DataFrame(data = None, columns = ["category"], index = range(len(df)))
    pos = 0
    if jsonFile=='fbUserDeviceCategories':
        for i in df:
            row=i['name']
            fbCsv["category"][pos] = row
            pos += 1
    else:
        for i in df:
            row = ""
            for element in i['path']:
                row += "/" + element
            fbCsv["category"][pos] = row
            pos += 1
    fbCsv.category = sorted(fbCsv.category)
    #print fbCsv

    fbCsv.to_csv('fbAdCategories/csv/'+jsonFile+'.csv', sep = ',', encoding='utf-8')

'''
'''
