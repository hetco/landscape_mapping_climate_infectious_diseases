#convert to institutes and shorten list (say 4 institutes)
#push collaboration to links object - pick smallest of two numbers - smallest is index - make sure not to double count in loops
#link object
# {institute10:{collabs:[12,17],strengths:{institute12:0.6,institute:17:1.2}}
# transform into list of links
# {source:10,target:12,strength:0.6,source:10,target:17,strength:1.2}

import json

##-------------
#compile institute to department lookup
#load orgswith file and process
#

with open('orgs_with0.825.json') as json_file:
    institutes_departments = json.load(json_file)

departmentLookup = {}

i=0
for institute in institutes_departments:
	for node in institute['nodes']:
		departmentID = 'department'+str(node['id'])
		departmentLookup[departmentID] = i
	i=i+1

print(i)

#print(departmentLookup)
#get papers_departments

with open('papers_departments.json') as json_file:
    papers_departments = json.load(json_file)

#group by paper

papers = {}

for pd in papers_departments:
	paperID = 'paper'+str(pd[0])
	if paperID in papers:
		papers[paperID].append(pd[1])
	else:
		papers[paperID] = [pd[1]]

#print(papers)

#convert to institutes
linkLookup = {}

for paper in papers:
	institutes = []
	#print(paper)
	for department in papers[paper]:
		#print(department)
		departmentID = 'department'+str(department)
		if departmentID in departmentLookup:
			institute = departmentLookup[departmentID]
			#print(institute)
			if institute not in institutes:
				institutes.append(institute)
		else:
			z=1
			#print(f"Not found {departmentID}")
		
	for institute1 in institutes:
		for institute2 in institutes:
			if institute1 < institute2:
				institute1ID = 'institute'+str(institute1)
				institute2ID = 'institute'+str(institute2)
				if institute1ID in linkLookup:
					if institute2 in linkLookup[institute1ID]['collab']:
						linkLookup[institute1ID]['strength'][institute2ID] = linkLookup[institute1ID]['strength'][institute2ID]+1
					else:
						linkLookup[institute1ID]['collab'].append(institute2)
						linkLookup[institute1ID]['strength'][institute2ID] = 1
				else:
					linkLookup[institute1ID] = {'collab':[institute2],'strength':{institute2ID:1}}

print(linkLookup['institute1'])

#createlinks

links = []
institutes = []

for inst in linkLookup:
	i1ID = inst[9:]
	for inst2 in linkLookup[inst]['strength']:
		i2ID = inst2[9:]
		if linkLookup[inst]['strength'][inst2]>4:
			links.append({'source':i1ID,'target':i2ID,'strength':linkLookup[inst]['strength'][inst2]})
			if i1ID not in institutes:
				institutes.append(i1ID)
			if i2ID not in institutes:
				institutes.append(i2ID)	

print(links)
print(institutes)

finalNodes = []
replace = {}
i=0
for inst in institutes:
	inst = int(inst)
	name = institutes_departments[inst]['approximateName']
	score = institutes_departments[inst]['score']
	finalNodes.append({'name':name,'score':score})
	replace[inst] = i
	i=i+1

print(finalNodes)
print(replace)

for link in links:
	link['source'] = replace[int(link['source'])]
	link['target'] = replace[int(link['target'])]

print(links)

with open('nodes.json', 'w') as outfile:
    json.dump(finalNodes, outfile)

with open('links.json', 'w') as outfile:
    json.dump(links, outfile)
