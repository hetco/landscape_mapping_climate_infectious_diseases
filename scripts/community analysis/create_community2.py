import psycopg2
import Levenshtein
import time
import simplejson as json

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

instituteSQL = 'select institute_id,institute_name,score,continent from institute left join country on institute.country_str = country.country'
cur.execute(instituteSQL)
institutes = cur.fetchall()

nodes = []
nodeLookup = {}
i=0
for institute in institutes:
	nodes.append({'institute_id':institute[0],'institute_name':institute[1],'score':institute[2],'continent':institute[3]})
	nodeLookup[institute[0]] = i
	i=i+1

print(nodeLookup[1129])

with open('nodes.json', 'w') as outfile:
    json.dump(nodes, outfile)

paperSQL = '''select distinct institute_id,paper.paper_id from department_institute
join paper_department on paper_department.department_id = department_institute.department_id
join paper on paper_department.paper_id = paper.paper_id
where paper.reviewed in (
'R*',
'R/T?',
'R?',
'R ',
'R /T?',
'T/?',
'T?',
'T ',
'T',
'R T?',
'R/T',
'review paper',
'R',
'T? / N?',
'T/R',
'CT?',
'R/N'		
)
order by paper_id'''

cur.execute(paperSQL)
papers = cur.fetchall()

paperGroups = {}

for paper in papers:
	if paper[1] not in paperGroups:
		paperGroups[paper[1]] = [paper[0]]
	else:
		paperGroups[paper[1]].append(paper[0])

linksLookUp = {}

for instituteList in paperGroups:
	i=0
	for x in paperGroups[instituteList]:
		j=0
		for y in paperGroups[instituteList]:
			if i<j:
				if x not in linksLookUp:
					linksLookUp[x] = {}
				if y not in linksLookUp[x]:
					linksLookUp[x][y] = 0
				linksLookUp[x][y] = linksLookUp[x][y]+1
			j=j+1
		i=i+1

templinks = []

print(linksLookUp[1129])
for x in linksLookUp:
	for y in linksLookUp[x]:
		templinks.append({'source':x,'target':y,'strength':linksLookUp[x][y]})

links = []
for link in templinks:
	source = nodeLookup[link['source']]
	target = nodeLookup[link['target']]
	strength = link['strength']
	if strength>1:
		links.append({'source':source,'target':target,'strength':strength})
with open('links.json', 'w') as outfile:
    json.dump(links, outfile)