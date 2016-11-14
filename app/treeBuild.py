import csv
#from django.conf import settings as st
from treelib import Node, Tree
import pandas
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print BASE_DIR




#This part works solely with Google ad categories
df = pandas.read_csv(BASE_DIR+'\\googleAdCategories\\affinity_categories.csv')

Gtree = Tree()
Gtree.create_node("Root", "root")

def adCatSplit(cat):
    toSplit = "root" + cat
    r = toSplit.split('/')
    print r
    return r

for c in df['Category']:
    newNode = adCatSplit(c)
    print newNode
    Gtree.create_node(newNode[-1], newNode[-1], newNode[-2])

Gtree.show()




#This part works with Facebook ad categories
fbTree = Tree()
fbTree.create_node("Root", "root")

df = pandas.read_json(BASE_DIR+'\\fbAdCategories\\fbInterestCategories.json')
df = df['data']

pathLength = 0



orderedList = list() #list is ordered by length of the path

while len(orderedList)!=329: #329 is the total number of categories (use CTRL + F and count the number of "id" instances)
    pathLength+=1
    for i in df:
        if len(i['path'])==pathLength:
            orderedList.append(i)

for c in orderedList:
    if fbTree.contains(c['name']):
        continue
    if len(c['path'])==1:
        fbTree.create_node(c['name'], c['name'], "root")
    else:
        fbTree.create_node(c['name'],c['name'], c['path'][-2])

fbTree.show()




'''
create buttons for root's children
<collapse rootChildren>


recursive function:
get_children_html(tree, root):
    children_list = tree.get_children(tree, root)

    
    html =
{% for cat in googleAdAffinity %}
<button type="button" class="btn btn-default" data-toggle="collapse" data-target="#collapse" 
	id="left" aria-expanded="false" aria-controls="collapseExample">
	{{cat}}
	</button>
	<div class="collapse">
	  <button type="button" class="btn btn-default" data-toggle="collapse" data-target="#collapse" 
	id="left" aria-expanded="false" aria-controls="collapseExample">
	</div>
{% endfor %}
</div>


'''

