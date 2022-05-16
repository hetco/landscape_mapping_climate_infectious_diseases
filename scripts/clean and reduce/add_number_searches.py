import json
import psycopg2


with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

output = []

sqlAllPapers = f"""select paper_id from paper where removal_candidate = 0"""
cur.execute(sqlAllPapers)
listOfPapers = cur.fetchall()

for paper in listOfPapers:

	paperID = paper[0]
	print(paperID)
	sqlCountSearches = f"""select count(search_terms) from paper
	join search_paper_ids on search_paper_ids.paper_id = paper.database_paper_id
	join searches on search_paper_ids.search_id = searches.search_id
	where paper.paper_id = {paperID}"""

	cur.execute(sqlCountSearches)
	sqlCountSearches = cur.fetchall()[0][0]

	sqlUpdate = f"""UPDATE public.paper
	SET num_searches={sqlCountSearches}
	WHERE paper_id = {paperID}""";

	cur.execute(sqlUpdate)
	conn.commit()
	


