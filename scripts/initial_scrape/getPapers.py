#libraries
import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import time
import json

def departmentClean(name):
	if name[-1] == '.':
		name = name[:-1]
	return name

#user variables
test = False

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

while True:
	sql1 = f"SELECT * FROM todo"

	cur.execute(sql1)
	sql1Result = cur.fetchone()
	conn.commit()

	
	if sql1Result == None:
		break
	print(sql1Result)

	pmID = sql1Result[1]
	searchID = sql1Result[3]

	#creqte and correct query
	sql13 = f"INSERT INTO public.todo_parked(todo_id, paper_id, database, search_id) VALUES ({sql1Result[0]}, {sql1Result[1]}, '{sql1Result[2]}', '{sql1Result[3]}');"
	cur.execute(sql13)
	conn.commit()

	#check paper not already in db
	db = 'pubmed'
	dbcheck = "database_paper_id"

	#check already not in papers

	sql6 = f"SELECT * FROM public.paper where {dbcheck} = {pmID};"
	cur.execute(sql6)
	sql6Rows = cur.fetchall()

	if len(sql6Rows)==0:

		
		#check if results are in database from previous search

		sql14 = f"SELECT * FROM public.paper_parked WHERE database_paper_id={pmID}"
		cur.execute(sql14)
		sql14Rows = cur.fetchall()
		if len(sql14Rows)>0:
			print('paper already in store')
			paperID = sql14Rows[0][0]
			title = sql14Rows[0][4]
			abstract = sql14Rows[0][5]

			departments = []

			sqldepartments = f"""SELECT department_name from department_parked
				INNER JOIN paper_department_parked on department_parked.department_id = paper_department_parked.department_id
				INNER JOIN paper_parked on paper_parked.paper_id = paper_department_parked.paper_id
				WHERE paper_parked.paper_id = {paperID}"""

			cur.execute(sqldepartments)
			sqldepartments = cur.fetchall()

			for row in sqldepartments:
				departments.append(row[0])

			meshHeadings = []
			keyWords = []

			sqltags = f"""SELECT keytext,meshorkey from keyword_parked
				INNER JOIN keyword_paper_parked on keyword_parked.keyword_id = keyword_paper_parked.keyword_id
				INNER JOIN paper_parked on paper_parked.paper_id = keyword_paper_parked.paper_id
				WHERE paper_parked.paper_id = {paperID}"""

			cur.execute(sqltags)
			sqltags = cur.fetchall()

			for row in sqltags:
				if row[1]=='key':
					keyWords.append(row[0])
				else:
					meshHeadings.append(row[0])

		else:

			print('paper not in store')

			params = {'db':db,'id':pmID,"tool":"tool_landscape_mapping","email":"simon@hetco.io","retmode":"xml"}
			paramsEncode = urllib.parse.urlencode(params)

			url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{paramsEncode}"

			print(url)

			contents = urllib.request.urlopen(url).read()

			soup = BeautifulSoup(contents,'html.parser')
			title = ""
			try:
				title = soup.pubmedarticleset.pubmedarticle.medlinecitation.article.articletitle.get_text()
				print(title)
			except:
				print("Might be a book not a paper, can't extract title")

			abstract = '';
			try:
				for ab in soup.pubmedarticleset.pubmedarticle.medlinecitation.article.abstract.find_all('abstracttext'):
					abstract = abstract + ' '+ab.get_text()

				abstract = abstract[1:]
			except:
				print("No abstract listed")

			departments = []

			try:
				for author in soup.pubmedarticleset.pubmedarticle.medlinecitation.article.authorlist.find_all('author'):
					affliations = author.affiliationinfo.affiliation.get_text()
					affliations = affliations.split('; ')
					for affliation in affliations:
						affliationClean = departmentClean(affliation)
						departments.append(affliationClean)
			except:
				print("No affliation listed")

			meshHeadings = []

			try:
				for meshHeading in soup.pubmedarticleset.pubmedarticle.medlinecitation.meshheadinglist.find_all('meshheading'):
					mesh = meshHeading.descriptorname.get_text()
					meshHeadings.append(mesh)
			except:
				print("No Mesh words")

			keyWords = [];

			try:
				for keyword in soup.pubmedarticleset.pubmedarticle.medlinecitation.keywordlist.find_all('keyword'):
					word = keyword.get_text()
					keyWords.append(word)
			except:
				print("No key words")

			print(meshHeadings)
			print(keyWords)



			#check already not in papers

		if test ==False:

			numDepartments = len(departments)

			#dbcheck = "paper_id"
			#if db == "pmc":
			#	dbcheck = "pmcid"

			sql4 = f"INSERT INTO public.paper(database_paper_id, papertitle, abstract, numauthors, search_id) VALUES ({pmID}, %s, %s, {numDepartments}, %s) RETURNING paper_id;"

			cur.execute(sql4,(title,abstract,searchID))
			conn.commit()
			paperDBID = cur.fetchone()[0]
			print(paperDBID)

			orgIDs = []
			for department in departments:
				sql2 = f"SELECT * FROM department where department_name=%s"
				cur.execute(sql2,(department,))
				sql2Rows = cur.fetchall()
				if len(sql2Rows)==0:
					sql3 = f"INSERT INTO public.department(department_name) VALUES (%s) RETURNING department_id;"
					cur.execute(sql3,(department,))
					conn.commit()
					orgID = cur.fetchone()[0]
					
				else:
					orgID = sql2Rows[0][0]
				orgIDs.append(orgID)

			for orgID in orgIDs:
				sql5 = f"INSERT INTO public.paper_department(paper_id, department_id) VALUES ({paperDBID}, {orgID});"
				cur.execute(sql5)
				conn.commit()

			wordIDs = []
			for word in meshHeadings:
				sql9 = f"SELECT * FROM keyword where keytext=%s AND meshorkey = 'mesh'"
				cur.execute(sql9,(word,))
				sql9Rows = cur.fetchall()
				if len(sql9Rows)==0:
					sql8 = f"INSERT INTO public.keyword(keytext, meshorkey) VALUES (%s, 'mesh') RETURNING keyword_id;"
					cur.execute(sql8,(word,))
					conn.commit()
					wordID = cur.fetchone()[0]
				else:
					wordID = sql9Rows[0][0]
				wordIDs.append(wordID)

			for word in keyWords:
				sql10 = f"SELECT * FROM keyword where keytext=%s AND meshorkey = 'key'"
				cur.execute(sql10,(word,))
				sql10Rows = cur.fetchall()
				if len(sql10Rows)==0:
					sql11 = f"INSERT INTO public.keyword(keytext, meshorkey) VALUES (%s, 'key') RETURNING keyword_id;"
					cur.execute(sql11,(word,))
					conn.commit()
					wordID = cur.fetchone()[0]
				else:
					wordID = sql10Rows[0][0]
				wordIDs.append(wordID)

			for wordID in wordIDs:
				sql12 = f"INSERT INTO public.keyword_paper(paper_id, keyword_id) VALUES ({paperDBID}, {wordID});"
				cur.execute(sql12)
				conn.commit()

			time.sleep(0.05)

	else:
		print("Paper already in records")

	print(f"deleting todo {pmID}")
	print("")
	print("")

	sql7 = f"DELETE FROM public.todo WHERE paper_id = {pmID};"
	cur.execute(sql7)
	conn.commit()

cur.close()
