import json
import psycopg2

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

keywordList = [
'Linear Regression',
'Logistic Regression',
'Multiple Linear Regression',
'Nonlinear Regression',
'Generalized Linear Model',
'Hierarchical Model',
'Stepwise Regression',
'MaxEnt',
'GARP',
'DesktopGARP',
'BIOMOD',
'dismo',
'Boosted Regression Trees',
'Classification and Regression Trees',
'Random Forests',
'Ecological niche factor analysis',
'Species Distribution Model',
'Ecological Niche Model',
'Habitat Suitability Model'
]

for keyword in keywordList:
	lowerKey = keyword.lower()
	sqlPapersText = f"""select paper_id,title,abstract,database_paper_id from paper where reviewed in (
		'R*',
		'R/T?',
		'??',
		'R?',
		'R ',
		'R /T?',
		'T/?',
		'T?',
		'T ',
		'P',
		'T',
		'R T?',
		'R/T',
		'review paper',
		'?',
		'R',
		'T? / N?',
		'T/R',
		'CT?',
		'R/N'
		)
		and (
		lower(papertitle) like '%{lowerKey}%'
		or lower(abstract) like '%{lowerKey}%'
		)"""

	cur.execute(sqlPapersText)
	sqlPapersTextRows = cur.fetchall()

	paperTextIDs = []
	for row in sqlPapersTextRows:
		paperTextIDs.append(row[0])

	sqlKeywords = f"""select paper_id,title,abstract,database_paper_id from paper 
		join keyword_paper on paper.paper_id = keyword_paper.paper_id
		join keyword on keyword.keyword_id = keyword_paper.keyword_id
		where reviewed in (
		'R*',
		'R/T?',
		'??',
		'R?',
		'R ',
		'R /T?',
		'T/?',
		'T?',
		'T ',
		'P',
		'T',
		'R T?',
		'R/T',
		'review paper',
		'?',
		'R',
		'T? / N?',
		'T/R',
		'CT?',
		'R/N'
		) and lower(keyword.keytext) like '%{lowerKey}%'"""

	cur.execute(sqlKeywords)
	sqlKeywordsRows = cur.fetchall()
	paperKeyIDs = []
	for row in sqlKeywordsRows:
		paperKeyIDs.append(row[0])

	intersection = list(set(paperTextIDs + paperKeyIDs))

	print(keyword + '|' + str(len(paperTextIDs)) + '|' + str(len(paperKeyIDs)) + '|' + str(len(intersection))) 

