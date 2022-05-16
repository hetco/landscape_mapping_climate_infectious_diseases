import json
import psycopg2

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

with open('lookup.json') as f:
  output = json.load(f)

pmIDsML = []

print('compiling external db list')
i=0
for paper in output:
	if paper[1]!='No ID':
		print(i)
		pmIDsML.append(paper[1])
		i=i+1

print(pmIDsML)

pmIDsDBSQL = f"""select database_paper_id from paper where reviewed
in (
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
)"""
print('compiling internal db list')
cur.execute(pmIDsDBSQL)
pmIDsDB = cur.fetchall()
pmIDsDBClean = []
for pmID in pmIDsDB:
	pmIDsDBClean.append(str(pmID[0]))
print(pmIDsDBClean)
print('calcualting intersection')
innerJoin = list(set(pmIDsDBClean) & set(pmIDsML))
print(len(pmIDsDBClean))
print(len(innerJoin))