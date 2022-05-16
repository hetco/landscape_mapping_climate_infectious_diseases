import psycopg2
import json

massMerge = False

def mergeInstitutes(absorbingInstitute,removeInstitute):
	sqlMerge = f"""UPDATE public.department_institute
	SET institute_id={absorbingInstitute}
	WHERE institute_id = {removeInstitute};"""

	cur.execute(sqlMerge)
	conn.commit()

	sqlScore1 = f"""SELECT score from institute
			where institute_id = {absorbingInstitute};"""

	cur.execute(sqlScore1)

	score1 = cur.fetchone()[0]

	sqlScore2 = f"""SELECT score from institute
			where institute_id = {removeInstitute};"""

	cur.execute(sqlScore2)

	score2 = cur.fetchone()[0]

	totalscore = score1 + score2

	print(totalscore)

	sqlScoreUpdate = f"""UPDATE public.institute
	   			SET score={totalscore}
	 			where institute_id = {absorbingInstitute};"""

	cur.execute(sqlScoreUpdate)
	conn.commit()

	sqlRemove = f"""DELETE FROM public.institute
	 		where institute_id = {removeInstitute};"""

	cur.execute(sqlRemove)
	conn.commit()
	print("Institutes Merged")


#connect to do database
with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

sqlUni = "SELECT * FROM institute WHERE lower(institute_name) LIKE '%university%' order by score desc"

cur.execute(sqlUni)
sqlUni = cur.fetchall()
for uni in sqlUni:
	print(uni[1])
	uniParts = uni[1].split(',')
	uniName = '';
	for part in uniParts:
		if part.lower().find('university')>-1:
			uniName = '%'+part.lower().strip()+'%'
	print(uniName)


	sqlFind = "SELECT * FROM institute WHERE lower(institute_name) LIKE %s"

	cur.execute(sqlFind,(uniName,))
	sqlInstitutesRows = cur.fetchall()
	print(len(sqlInstitutesRows))
	if len(sqlInstitutesRows)>2:
		print('Merge Choice')
		i=0
		if massMerge == True:
			for row in sqlInstitutesRows:
				print("")
				print("")
				print("")
				print(row[0])
				print(row[1])
			print(uniName)
			inp = input("Merge (y/n)") 
			if inp == 'y':
				j=0
				for row in sqlInstitutesRows:
					if j==0:
						print('Main merge with')
						print(row[1])
						keyID = row[0]
					else:
						print("")
						print(row[0])
						print(row[1])
						mergeInstitutes(keyID,row[0])
					j=j+1
		else:
			for row in sqlInstitutesRows:
				if i==0:
					print('Main merge with')
					print(row[1])
					keyID = row[0]
				else:
					print("")
					print(row[0])
					print(row[1])
					inp = input("Merge (y/n)") 
					if inp == 'y':
						mergeInstitutes(keyID,row[0])
				i=i+1
