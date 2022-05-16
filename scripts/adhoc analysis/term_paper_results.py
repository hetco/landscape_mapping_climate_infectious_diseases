import json
import psycopg2
import csv

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

output = []

# keywordList = [
# 'Linear Regression',
# 'Logistic Regression',
# 'Multiple Linear Regression',
# 'Nonlinear Regression',
# 'Generalized Linear Model',
# 'Hierarchical Model',
# 'Stepwise Regression',
# 'MaxEnt',
# 'GARP',
# 'DesktopGARP',
# 'BIOMOD',
# 'dismo',
# 'Boosted Regression Trees',
# 'Classification and Regression Trees',
# 'Random Forests',
# 'Ecological niche factor analysis',
# 'Species Distribution Model',
# 'Ecological Niche Model',
# 'Habitat Suitability Model'
# ]

keywordList = [
'linear',
'stepwise',
'Logistic',
'Ecological Niche',
'regression'
]

for keyword in keywordList:

	keywordOutput = []
	keywordIDs = []
	lowerKey = keyword.lower()
	sqlPapersText = f"""select paper.paper_id,papertitle,abstract,database_paper_id from paper where reviewed in (
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

	for row in sqlPapersTextRows:
		if row[0] not in keywordIDs:
			keywordIDs.append(row[0])
			keywordOutput.append([lowerKey] + list(row))

	sqlKeywords = f"""select paper.paper_id,papertitle,abstract,database_paper_id from paper 
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
	for row in sqlKeywordsRows:
		if row[0] not in keywordIDs:
			keywordIDs.append(row[0])
			keywordOutput.append([lowerKey] + list(row))

	output = output + keywordOutput

with open("keyword_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

