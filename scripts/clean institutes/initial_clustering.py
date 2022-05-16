#a script to extract orgs and number of publications they have
#outputs org and publication numbers
# options to do grouping based on word distance
import psycopg2
import Levenshtein
import time
import simplejson as json

#functions

def cluster(nodes,links):
	for link in links:
		node1 = link[0]
		node2 = link[1]
		cluster1 = nodes[node1]['cluster']
		cluster2 = nodes[node2]['cluster']
		nodes = changeCluster(nodes,cluster1,cluster2)
	return nodes

def changeCluster(nodes,new,old):
	for node in nodes:
		if(node['cluster']==old):
			node['cluster'] = new
	return nodes

def group(nodes):
	groups = {}
	for node in nodes:
		clusterName = 'cluster' + str(node['cluster'])
		if clusterName in groups:
			groups[clusterName]['nodes'].append(node)
			groups[clusterName]['score'] = groups[clusterName]['score']+node['score']
		else:
			groups[clusterName] = {'score':node['score'],'nodes':[node]}
	return groups

def cleanForCompare(inputStr):
	print(inputStr)
	findAt = inputStr.find('Electronic address:')
	if findAt>0:
		lastPeriod = inputStr[:findAt].rfind('.')
		inputStr = inputStr[:lastPeriod]
	inputList = inputStr.split(', ')
	outputList = []
	keywords = ['department of','division of','college of','dept. of','laboratory','school of']
	keepList = ['london school']
	for element in inputList:
		remove = False
		element = element.lower()
		findAt = element.find('university')
		if findAt==-1:
			for keyword in keywords:
				if element.find(keyword)>-1:
					remove = True
			for keyword in keepList:
				if element.find(keyword)>-1:
					remove = False
		if remove==False:
			outputList.append(element)
	outputStr = ', '.join(outputList)

	keywords = [{'find':'university','replace':'u__'},{'find':'disease control and prevention','replace':'dcap__'}]
	for keyword in keywords:
		outputStr = outputStr.replace(keyword['find'],keyword['replace'])
	print(outputStr)
	print("")
	#time.sleep(0.5)
	return outputStr

#choose to run or departments or institutes

table = 'departments'

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)


#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

sql1 = """select institute_id, institute_name, score from institute where institute_name is not null"""

cur.execute(sql1)
sql1Rows = cur.fetchall()

links = []
nodes = []
i = 0
for row in sql1Rows:
	nodes.append({'id':row[0],'name':row[1],'cleanname':cleanForCompare(row[1]),'cluster':i,'score':row[2]})
	i=i+1

i=0
for row in nodes:
	print(i)
	j=0
	compare1 = row['cleanname']
	
	for row2 in nodes:
		if i<j:
			compare2 = row2['cleanname']
			ratio = Levenshtein.ratio(compare1,compare2)
			if ratio>0.825:
				links.append([i,j,ratio])
				#print(compare1)
				#print(compare2)
				#print(ratio)
				#print("")
		j=j+1
	i=i+1

print('clustering')
nodes = cluster(nodes,links)
print('making groups')
groups = group(nodes)
groupList =[]
for group in groups:
	groupList.append(groups[group])
	groupList.sort(key=lambda x: x['score'], reverse=True)

for group in groupList:
	score = group['score']
	print(f"Publish Score: {score}")
	nodes = group['nodes']
	names = []
	for node in nodes:
		node['cleanname'] = node['cleanname'].replace('u__','university')
		node['cleanname'] = node['cleanname'].replace('dcap__','disease control and prevention')
		print(node['cleanname'])
		names.append(node['cleanname'])
	print("")
	group['approximateName'] = Levenshtein.setmedian(names).capitalize()

with open('orgs_with0.825.json', 'w') as outfile:
    json.dump(groupList, outfile)