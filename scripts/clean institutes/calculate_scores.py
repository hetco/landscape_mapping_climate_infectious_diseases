import psycopg2
import json


#connect to do database
with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

sqlInstitutes = """SELECT institute_id from institute"""
cur.execute(sqlInstitutes)

sqlInstitutes = cur.fetchall()
for row in sqlInstitutes:
	print(row[0])

	sqlScore = """SELECT sum(cast(1 as float)/cast(paper.numauthors as float)) as score from institute
			inner join department_institute on department_institute.institute_id = institute.institute_id
			inner join department on department_institute.department_id = department.department_id
			inner join paper_department on paper_department.department_id = department.department_id
			inner join paper on paper.paper_id = paper_department.paper_id
			where institute.institute_id = %s and paper.reviewed in (
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
			group by institute.institute_id"""
	cur.execute(sqlScore,(row[0],))
	sqlScore = cur.fetchall()
	try:
		score = sqlScore [0][0]
	except:
		score = 0

	sqlScoreUpdate = """UPDATE public.institute SET score=%s WHERE institute_id = %s"""
	cur.execute(sqlScoreUpdate,(score,row[0]))
	conn.commit()

