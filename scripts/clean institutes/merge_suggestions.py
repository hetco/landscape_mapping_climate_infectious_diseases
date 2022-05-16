import psycopg2
import Levenshtein
import json

def mergeInstitutes(absorbingInstitute,removeInstitute):

	sqlScore1 = f"""SELECT score from institute
			where institute_id = {absorbingInstitute};"""

	cur.execute(sqlScore1)

	score1 = cur.fetchone()[0]

	sqlScore2 = f"""SELECT score from institute
			where institute_id = {removeInstitute};"""

	cur.execute(sqlScore2)

	score2 = cur.fetchone()[0]

	totalscore = score1 + score2

	sqlMerge = f"""UPDATE public.department_institute
	SET institute_id={absorbingInstitute}
	WHERE institute_id = {removeInstitute};"""

	cur.execute(sqlMerge)
	conn.commit()

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


#sqlInstitutes = "select * from institute where country = 'Macao' order by score desc limit 500"
sqlInstitutes = "select * from institute where country_str = 'India' order by score desc"
#sqlInstitutes = "select * from institute order by institute_id"
cur.execute(sqlInstitutes)
sqlInstitutesRows = cur.fetchall()
i=0
for institute1 in sqlInstitutesRows:
	j=0
	institute1Name = institute1[1]
	for institute2 in sqlInstitutesRows:
		institute2Name = institute2[1]
		if i<j:
			ratio = Levenshtein.ratio(institute1Name,institute2Name)
			if ratio>0.65:
				print("")
				print("possible match")
				print(institute1[0])
				print(institute1Name)
				print(institute1[2])
				print(institute2[0])
				print(institute2Name)
				print(institute2[2])
				inp = input("Merge (y/n)") 
				if inp == 'y':
					try:
						mergeInstitutes(institute1[0],institute2[0])
					except:
						print('error merging')
		j=j+1
	i=i+1