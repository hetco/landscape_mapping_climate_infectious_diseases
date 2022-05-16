import json
import psycopg2

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)


#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

with open('orgs_with0.825.json') as json_file:
	institutes = json.load(json_file)
	

for institute in institutes:
	name = institute['approximateName']
	score = institute['score']
	parentInstitute = institute['nodes'][0]['id']

	sqlInstitute = f"""UPDATE public.institute
			SET institute_name=%s, score={score}
			WHERE institute_id = {parentInstitute}"""

	cur.execute(sqlInstitute,(name,))
	conn.commit()

	instituteList = institute['nodes']
	for subInstititue in instituteList:
		instituteID = subInstititue['id']

		sqlDepartment = f"""UPDATE public.department_institute
				SET institute_id={parentInstitute}
				WHERE institute_id = {instituteID}"""

		cur.execute(sqlDepartment)
		conn.commit()

conn.close()

#clean up

"""delete from institute where institute_id in (
	select institute.institute_id from institute
	left outer join department_institute on institute.institute_id = department_institute.institute_id
	where department_institute.institute_id is null)
"""