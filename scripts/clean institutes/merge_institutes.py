import psycopg2
import json

#connect to do database
with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

absorbingInstitute = 316
removeInstitute = 1847

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
