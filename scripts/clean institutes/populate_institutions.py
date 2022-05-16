import csv
import psycopg2
import json

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

sqlDepartments = """select distinct department.department_name, department.department_id from department
join paper_department on  paper_department.department_id = department.department_id
join paper on paper.paper_id = paper_department.paper_id
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
)"""



cur.execute(sqlDepartments)
listOfDepartments = cur.fetchall()

for department in listOfDepartments:
	sqlCheckDepartment = f"""SELECT COUNT(1)
		FROM department_institute
		WHERE department_id = {department[1]};"""
	print(department)
	cur.execute(sqlCheckDepartment)
	count= cur.fetchall()[0][0]
	if count==0:
		sqlInstitute = f"""INSERT INTO institute(institute_name) VALUES (%s) RETURNING institute_id;"""
		cur.execute(sqlInstitute,(department[0],))
		conn.commit()
		orgID = cur.fetchone()[0]

		sqlDepartmentInstitute = f"""INSERT INTO public.department_institute(department_id, institute_id) VALUES ({department[1]}, {orgID});"""
		cur.execute(sqlDepartmentInstitute)
		conn.commit()





