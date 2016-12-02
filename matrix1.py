import pandas
import numpy as np

'''
This part converts fbAdCategories.json to .csv with index and category as headers
'''

toConvert = ['fbInterestCategories', 'fbBehaviorsCategories', 'fbEthnicAffinityCategories', 'fbFamilyStatusesCategories', 'fbGenerationCategories', 'fbHouseholdCompoCategories','fbIncomeCategories', 'fbIndustriesCategories', 'fbLifeEventsCategories', 'fbNetWorthCategories', 'fbPoliticsCategories', 'fbUserDeviceCategories']



for jsonFile in toConvert:
    df = pandas.read_json('fbAdCategories/json/'+jsonFile+'.json')
    df = df['data']
    print len(df)
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

    print fbCsv.category

'''
'''

googleCsv = pandas.read_csv('googleAdCategories/affinity_categories.csv')
fbCsv = pandas.read_csv('fbAdCategories/csv/fbInterestCategories.csv')

#print googleCsv.Category

matrix = pandas.DataFrame(index = fbCsv.category, columns = googleCsv.Category)
print matrix.columns


matrix.to_csv('matrix.csv', sep=',')

