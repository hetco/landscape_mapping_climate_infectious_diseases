#a script to remove triplet term from database

import json
import psycopg2

#removed terms so far
#database

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])
cur = conn.cursor()

#get IDs from search and number of times ID appears. Remove those that appear once

sqlpapers = """select search_paper_ids.paper_id, count(*) from searches
join search_paper_ids on search_paper_ids.search_id = searches.search_id
join paper on paper.database_paper_id = search_paper_ids.paper_id
where search_terms like '%database' and paper.removal_candidate = 0
group by search_paper_ids.paper_id
having count(*) = 1"""

cur.execute(sqlpapers)
sqlPapersRows = cur.fetchall()
for paper in sqlPapersRows:
	paper_id = paper[0]
	sqlUpdate = f"""UPDATE public.paper
	SET removal_candidate=2
	WHERE database_paper_id = '{paper_id}';"""
	cur.execute(sqlUpdate)
	conn.commit()
