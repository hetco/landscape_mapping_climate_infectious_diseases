import psycopg2
import json
import csv

#connect to do database
with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()


selectionCriteria = [
	{'key':'continent','value':'Africa','limit':10},
	{'key':'continent','value':'Arab States','limit':10},
	{'key':'continent','value':'South/Latin America','limit':10},
]

institutes = []

for criteria in selectionCriteria:
	key = criteria['key']
	value = criteria['value']
	limit = criteria['limit']

	sqlWithParams = f"""SELECT institute_id, institute_name, lat, lon, score from institute
				JOIN country on institute.country_str = country.country
				WHERE {key} = '{value}'
				ORDER BY score desc
				LIMIT {limit}"""
	print(sqlWithParams)

	cur.execute(sqlWithParams)
	sqlWithParamsRows = cur.fetchall()
	for row in sqlWithParamsRows:
		print(row)
		institutes.append([row[0],row[1],float(row[4]),float(row[2]),float(row[3])])

#add top 100

sqlTop100 = f"""SELECT institute_id, institute_name, lat, lon, score from institute
			WHERE score>0
			ORDER BY score desc
			LIMIT 100"""

cur.execute(sqlTop100)
sqlTop100Rows = cur.fetchall()
for row in sqlTop100Rows:
	print(row)
	if row[3] == None:
		institutes.append([row[0],row[1],'',''])
	else:
		institutes.append([row[0],row[1],float(row[4]),float(row[2]),float(row[3])])

#dedup

IDs = []
output = []

for row in institutes:
	if row[0] not in IDs:
		IDs.append(row[0])
		output.append(row)

#get papers

papers = []


for ID in IDs:
	sqlPapers = f"""SELECT distinct paper.database_paper_id, paperTitle, department_institute.institute_ID from paper
			join paper_department on paper_department.paper_ID = paper.paper_ID
			join department on paper_department.department_ID = department.department_ID
			join department_institute on department_institute.department_ID = department.department_ID
			WHERE department_institute.institute_ID = {ID} and paper.reviewed in (
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
			limit 5"""
	cur.execute(sqlPapers)
	sqlPapersRows = cur.fetchall()
	for row in sqlPapersRows:

		papers.append([row[0],row[1],row[2]])

with open("institutes_for_mapping.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

with open("institutes_papers.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(papers)