import json
import psycopg2

listOfPapers = [
[14251,0],
[16296,0],
[15069,0.5],
[15118,0],
[16847,0],
[15977,0],
[15763,0.5],
[14996,0],
[15622,0.5],
[14767,0.5],
[16651,0],
[14473,1],
[14955,0],
[14284,0],
[15706,0],
[16694,0],
[15272,0],
[17024,0],
[15438,0],
[17026,0],
[14250,1],
[14491,0],
[14811,0],
[16735,0],
[14574,0],
[15560,0],
[14692,0],
[13987,0],
[15179,0],
[13960,0.5],
[15460,0],
[14673,1],
[14388,0],
[14352,1],
[16414,0],
[14903,0],
[16881,0],
[15767,0],
[14209,0],
[13557,0],
[14183,1],
[15679,0],
[15809,0],
[15826,0],
[15943,0],
[15494,0],
[21313,0],
[2578,0],
[14193,0],
[6788,1],
[3693,1],
[1585,0],
[125,0],
[7220,0],
[19435,0],
[23701,0],
[21066,0],
[23584,0],
[5135,1],
[26121,0],
[15105,0.5],
[23660,0],
[22276,0],
[6696,1],
[6884,1],
[8256,0],
[4302,0.5],
[7059,0],
[14191,0],
[24361,0],
[23993,0],
[4413,0],
[4016,0],
[1214,0],
[22808,0],
[4166,0],
[6397,0],
[7899,0],
[14042,0],
[15457,0],
[27466,0],
[28820,0],
[9196,0],
[22026,0],
[24846,0],
[24351,0],
[22726,0],
[30474,0],
[705,0],
[14252,0],
[571,0],
[4649,0],
[4903,0],
[10806,0],
[24494,0],
[22864,0],
[23462,0],
[40,1],
[11470,0],
[23476,0]
]

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

output = []

for paper in listOfPapers:

	paperID = paper[0]

	sqlCountSearches = f"""select count(search_terms) from paper
	join search_paper_ids on search_paper_ids.paper_id = paper.database_paper_id
	join searches on search_paper_ids.search_id = searches.search_id
	where paper.paper_id = {paperID}"""

	cur.execute(sqlCountSearches)
	sqlCountSearches = cur.fetchall()[0][0]

	sqlCountNonSeasonal = f"""select count(search_terms) from paper
	join search_paper_ids on search_paper_ids.paper_id = paper.database_paper_id
	join searches on search_paper_ids.search_id = searches.search_id
	where paper.paper_id = {paperID} and search_terms not like 'Seasonal%'"""

	cur.execute(sqlCountNonSeasonal)
	sqlCountNonSeasonal = cur.fetchall()[0][0]

	sqlCountInfluenza = f"""select count(search_terms) from paper
	join search_paper_ids on search_paper_ids.paper_id = paper.database_paper_id
	join searches on search_paper_ids.search_id = searches.search_id
	where paper.paper_id = {paperID} and search_terms like '%Influenza%'"""

	sqlCountNonTechnicalSearches = f"""select paper.paper_id,search_terms from paper
	join search_paper_ids on search_paper_ids.paper_id = paper.database_paper_id
		join searches on search_paper_ids.search_id = searches.search_id
		where paper.paper_id = {paperID}"""

	cur.execute(sqlCountNonTechnicalSearches)
	sqlCountNonTechnicalSearches = cur.fetchall()
	totalSearches = set([]);
	for search in sqlCountNonTechnicalSearches:
		searchTerm = " + ".join(search[1].split(" + ")[:2])
		totalSearches.add(searchTerm)
	totalSearches = len(totalSearches)

	cur.execute(sqlCountInfluenza)
	sqlCountInfluenza = cur.fetchall()[0][0]

	output.append([paperID, paper[1], sqlCountSearches, sqlCountNonSeasonal,sqlCountInfluenza,totalSearches])
	print(str(paperID)+','+str(paper[1])+','+str(sqlCountSearches)+','+str(sqlCountNonSeasonal)+','+str(sqlCountInfluenza)+','+str(totalSearches))


