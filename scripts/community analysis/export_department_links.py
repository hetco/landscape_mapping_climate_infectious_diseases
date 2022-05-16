import psycopg2
import Levenshtein
import time
import json

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()
sql1 = "select paper_id,database_paper_id,papertitle from paper"

cur.execute(sql1)
sql1Rows = cur.fetchall()

output = {};

for row in sql1Rows:
	paperid = f'paper{row[0]}'
	output[paperid] = {'id':row[0],'pmid':row[1],'title':row[2]}

with open('papers.json', 'w') as outfile:
    json.dump(output, outfile)

sql2 = "select paper_id,department_id from paper_department"
cur.execute(sql2)
sql2Rows = cur.fetchall()

#possible to dedup
with open('papers_departments.json', 'w') as outfile:
    json.dump(sql2Rows, outfile)

