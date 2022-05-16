#a script to remove triplet term from database

import json
import psycopg2

triplet = 'Climate  + epidemic + database'

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])
cur = conn.cursor()

#get IDs from search and number of times ID appears. Remove those that appear once

sqlTripletPapers = f"""select paper.paper_id,paper.database_paper_id from paper
	join
	(select search_paper_ids.paper_id,count(*) as co
	from 
	(select paper_id
	from searches
	join search_paper_ids on searches.search_id = search_paper_ids.search_id
	where search_terms like '%software') as triplet_results
	join search_paper_ids on search_paper_ids.paper_id = triplet_results.paper_id
	group by search_paper_ids.paper_id
	having count(*) = 1) as unique_papers
	on paper.database_paper_id = unique_papers.paper_id
	where paper.search_id like '%software'"""

#simpler version?
select search_paper_ids.paper_id, count(*) from searches
join search_paper_ids on search_paper_ids.search_id = searches.search_id
join paper on paper.database_paper_id = search_paper_ids.paper_id
where search_terms like '%database' and paper.removal_candidate = 0
group by search_paper_ids.paper_id
having count(*) = 1

print('Getting Papers')
cur.execute(sqlTripletPapers)
sqlTripletPapersRows = cur.fetchall()
for paper in sqlTripletPapersRows:
	paperID = paper[0]

	print(paperID)
	#remove from department_papers
	sqlRemoveFromDepartmentPapers = f"""delete from paper_department where paper_id={paperID}"""
	cur.execute(sqlRemoveFromDepartmentPapers)
	conn.commit()

	#remove from keyword_ids
	sqlRemoveFromKeywordPapers = f"""delete from keyword_paper where paper_id={paperID}"""
	cur.execute(sqlRemoveFromKeywordPapers)
	conn.commit()

	#remove from papers
	sqlRemoveFromPapers = f"""delete from paper where paper_id={paperID}"""
	cur.execute(sqlRemoveFromPapers)
	conn.commit()

#remove empty departments
print('Removing departments')
sqlRemoveEmptyDepartments = f"""delete from department where department_id in (select department.department_id from department
	left outer join paper_department on department.department_id = paper_department.department_id
	where paper_department.department_id is null)"""
cur.execute(sqlRemoveEmptyDepartments)
conn.commit()

#remove empty from keywords
print('Removing Keywords')
sqlRemoveEmptyKeywords = f"""delete from keyword where keyword_id in (select keyword.keyword_id from keyword
	left outer join keyword_paper on keyword.keyword_id = keyword_paper.keyword_id
	where keyword_paper.keyword_id is null)"""
cur.execute(sqlRemoveEmptyKeywords)
conn.commit() 

#remove from search_paper_ids
print('Removing Search results')
sqlRemoveSearchResults = f"""delete from search_paper_ids where search_id in (select search_id from searches where search_terms = '{triplet}')"""
cur.execute(sqlRemoveSearchResults)
conn.commit()

#remove from search
print('Removing search')
sqlRemoveFromSearch = f"""delete from searches where search_terms = '{triplet}'"""

